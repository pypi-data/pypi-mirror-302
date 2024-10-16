# SPDX-FileCopyrightText: 2024-present Panayotis Vryonis <vrypan@gmail.comm>
#
# SPDX-License-Identifier: MIT
import click
from datetime import datetime
import random
import sqlite3
import sys

from fc_nmap.__about__ import __version__
from fc_nmap.get_hubs import get_hub_info, get_hubs
from fc_nmap import dbexports, dbexports_maps
from fc_nmap.ip2location import resolve_ip

@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="fc-nmap")
def fc_nmap():
    """Farcaster Network Mapper
    """
    pass

@fc_nmap.command()
@click.option('--hub', default='hoyt.farcaster.xyz:2283', help='IP:port of hub to start crawling from.')
@click.option('--hops', default=10, help='Number of hubs to query.')
# @click.option('--out', default='-', type=click.File('w'), help="Output file, leave empty for stdout")
def scan(hub, hops):
    """Scan the network
    """
    try:
        db_conn = sqlite3.connect('hubs.db')
        db_cursor = db_conn.cursor()
    except:
        click.echo('hubs.db not found. Run "fc-nmap initdb" to create it.')
        sys.exit(1)
    hubs = {}
    with click.progressbar(
            length=hops, 
            label='Scanning', 
            width=0,
            show_eta=False,
            bar_template='%(label)s  %(bar)s  %(info)s',
            #fill_char='█',
            fill_char='#',
            item_show_func=lambda a: a.rjust(21) if a else None
        ) as bar:
        bar.update(1, hub)
        hubs = get_hubs(hub,{})
        if not hubs:
            click.echo(f'Unable to contact {hub}')
            sys.exit(1)
        for i in range(hops-1):
            bar.update(1, hub)
            hub = random.choice(list(hubs.keys()))
            hubs = get_hubs(hub,hubs)
            
        bar.update(1,'Done.')
    click.echo(f'Hubs found: {len(hubs)}')
    for h in hubs:
        h_ip,h_port = h.split(':')
        h_app_ver   = hubs[h]['appv']
        h_proto_ver = hubs[h]['hubv']
        h_dnsname   = hubs[h]['dns_name']
        h_ts        = hubs[h]['timestamp']
        db_cursor.execute("""
            INSERT OR REPLACE INTO hub (ip, port, dnsname, proto_version, app_version, ts) VALUES (?,?,?,?,?,datetime(?/1000, 'unixepoch'))
            """, 
            (h_ip, h_port, h_dnsname, h_proto_ver, h_app_ver, h_ts)
        )
        # click.echo(f'{h}\t{hubs[h]['appv']}\t{datetime.fromtimestamp(int(hubs[h]['timestamp']/1000), tz=None)}', file=out)
    db_cursor.execute("""INSERT OR REPLACE INTO kv VALUES ('LAST_SCAN', unixepoch('now'))""")
    db_conn.commit()
    click.echo('Database updated.')
    

@fc_nmap.command()
@click.argument('output', default='-', type=click.File('w'))
@click.option('--hub-info', is_flag=True, help="Collect hub info for hubs")
@click.option('--hub-location', is_flag=True, help="Look up hubs geolocation")
@click.option('--geo-api-key', help="API key to be used for IP-to-geolocation service", show_default=True, envvar='FCNMAP_GEO_API_KEY')
@click.option('--age-threshold', default=86400, help="Only check records no older than INTEGER.", show_default=True)
@click.option('--timeout', default=5, help='Seconds to wait before gRPC timeout.')
def updatedb(output, age_threshold, hub_info, hub_location, geo_api_key, timeout):
    """Collect addtional information about each hub
    """
    if hub_location:
        if not geo_api_key:
            click.echo("You will need to pass --geo-api-location a key from ip2location.io")
            sys.exit(1)
        else:
            update_hub_geo(geo_api_key)
    if hub_info:
        click.echo("Connecting to each hub to collect more info")
        update_hub_info(output, age_threshold, timeout)

def update_hub_info(output, age_threshold, timeout):
    conn = sqlite3.connect('hubs.db')
    # r_cursor = conn.cursor()
    # w_cursor = conn.cursor()
    cursor = conn.cursor()
    
    cursor.execute("""SELECT v FROM kv WHERE k='LAST_SCAN' """)
    last_scan = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM hub LEFT JOIN hub_info
        ON hub.ip = hub_info.ip AND hub.port = hub_info.port 
        WHERE unixepoch(hub.ts) > unixepoch('now') - ? -- hub was active in the last N seconds
        AND ( unixepoch(hub_info.updated_at) < unixepoch('now') -  ? -- hub info was not updated in the last N seconds
        OR hub_info.updated_at IS NULL )
        """, (age_threshold, age_threshold,))
    count = cursor.fetchone()[0]

    # r_cursor.execute("""SELECT * FROM hub""")
    cursor.execute("""
        SELECT hub.ip, hub.port, hub.dnsname FROM hub LEFT JOIN hub_info
        ON hub.ip = hub_info.ip AND hub.port = hub_info.port 
        WHERE unixepoch(hub.ts) > unixepoch('now') - ? -- hub was active in the last N seconds
        AND ( unixepoch(hub_info.updated_at) < unixepoch('now') -  ? -- hub info was not updated in the last N seconds
        OR hub_info.updated_at IS NULL )
        """, (age_threshold, age_threshold))
    records = cursor.fetchall()

    i = 0
    with click.progressbar(records, 
        label=f"Scanning {count} hubs",
        length=count, 
        width=0, 
        bar_template='%(label)s  %(bar)s  %(info)s', 
        item_show_func=lambda a: a.rjust(21) if a else None
        ) as bar:
        for r in records:
            i+=1
            bar.update(1, f"{i}/{count}".rjust(10) )
            info = get_hub_info(address=r[0],port=r[1],dnsname=r[2], timeout=timeout)
            if info:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO hub_info 
                    (ip, port, version, is_syncing, nickname, root_hash, peerid, fid, num_messages, num_fid_events, num_fname_events, approx_size, updated_at) 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,datetime())
                    """,
                    (r[0],r[1], #ip:port
                    info.version,
                    info.is_syncing,
                    info.nickname,
                    info.root_hash,
                    info.peerId,
                    info.hub_operator_fid,
                    info.db_stats.num_messages,
                    info.db_stats.num_fid_events,
                    info.db_stats.num_fname_events,
                    info.db_stats.approx_size
                    )
                    )
                line = f"{r[0]}:{r[1]} -- {info.hub_operator_fid}"
            else:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO hub_info (ip, port, updated_at) VALUES (?,?,datetime())
                    """,
                    (r[0],r[1])
                )
                line = f"{r[0]}:{r[1]} -- Unknown".ljust(40)
            conn.commit()
            # print(line)
            #print(line, f"{r[0]}:{r[1]}".ljust(30), end='\r', flush=True)
        

def update_hub_geo(geo_api_key):
    conn = sqlite3.connect('hubs.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM hub LEFT JOIN addr
        ON hub.ip = addr.ip
        WHERE unixepoch('now') - unixepoch(addr.updated_at) > ?
        OR addr.updated_at IS NULL
        """, (60*60*24*100,))
    count = cursor.fetchone()[0]

    # r_cursor.execute("""SELECT * FROM hub""")
    cursor.execute("""
        SELECT hub.ip FROM hub LEFT JOIN addr
        ON hub.ip = addr.ip
        WHERE unixepoch('now') - unixepoch(addr.updated_at) > ?
        OR addr.updated_at IS NULL
        """, (60*60*24*100,))
    records = cursor.fetchall()

    i = 0
    with click.progressbar(records, 
        label=f"Looking up {count} IPs",
        length=count, 
        width=0, 
        bar_template='%(label)s  %(bar)s  %(info)s', 
        item_show_func=lambda a: a.rjust(21) if a else None
        ) as bar:
        for r in records:
            i+=1
            #bar.update(1, f"{i}/{count}".rjust(10) )
            info = resolve_ip(geo_api_key, r[0])
            if info:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO addr VALUES (?,?,?,?,?,?,?,?,?,?,?,?,datetime())
                    """,(
                        info['ip'],
                        info['country_code'], 
                        info['country_name'],
                        info['region_name'],
                        info['city_name'],
                        info['latitude'],
                        info['longitude'],
                        info['zip_code'],
                        info['time_zone'],
                        info['asn'],
                        info['as'],
                        info['is_proxy']
                    )
                )
                conn.commit()
                bar.update(1, f"{i}/{count}".rjust(10) )
            else:
                bar.update(1, f"ERROR {i}/{count}".rjust(10) )
            #print(line, f"{r[0]}:{r[1]}".ljust(30), end='\r', flush=True)
    conn.commit()
    
@fc_nmap.command()
def initdb():
    """Initialize the database"""
    conn = sqlite3.connect('hubs.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kv
        ( k TEXT NOT NULL PRIMARY KEY, v INTEGER )
        
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hub
        ( ip text, port integer, dnsname TEXT, proto_version text, app_version text, ts TEXT, 
            PRIMARY KEY(ip,port)
        )
        
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_hub_ip ON hub(ip)
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hub_info
        ( ip text, port INTEGER, 
            version TEXT, 
            is_syncing BOOL, 
            nickname TEXT, 
            root_hash TEXT, 
            peerid TEXT, 
            fid INTEGER, 
            num_messages INTEGER, 
            num_fid_events INTEGER, 
            num_fname_events INTEGER, 
            approx_size INTEGER,
            updated_at TEXT NOT NULL DEFAULT current_timestamp,
            PRIMARY KEY(ip,port)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS addr (
            ip text NOT NULL PRIMARY KEY, 
            country_code TEXT, 
            country_name TEXT,
            region_name TEXT,
            city_name TEXT,
            latitude REAL,
            longitude REAL,
            zip_code TEXT,
            time_zone TEXT,
            as_number INTEGER,
            as_name TEXT,
            is_proxy BOOL,
            updated_at TEXT NOT NULL DEFAULT current_timestamp
        )
    """)
    conn.commit()
    click.echo("hubs.db created.")
    
@fc_nmap.command()
@click.option('--out', default='-', help="Output file, leave empty for stdout")
@click.option('--max-age', default=86400, help="Only check records that were created/updated in the last INTEGER seconds.", show_default=True)
@click.option('--report', type=click.Choice(['all', 'countries', 'fids', 'app', 'asn', 'geoip', 'map'], case_sensitive=False))
def export(out, max_age, report):
    """Create a tab separated dump of the database"""
    if report == 'all':
        dbexports.export_full(dbpath='hubs.db', out=out, max_age=max_age)
    if report == 'countries':
        dbexports.export_countries(dbpath='hubs.db', out=out, max_age=max_age)
    if report == 'fids':
        dbexports.export_fids(dbpath='hubs.db', out=out, max_age=max_age)
    if report == 'app':
        dbexports.export_app_version(dbpath='hubs.db', out=out, max_age=max_age)
    if report == 'asn':
        dbexports.export_asn(dbpath='hubs.db', out=out, max_age=max_age)
    if report == 'geoip':
        dbexports.export_latlong(dbpath='hubs.db', out=out, max_age=max_age)
    if report == 'pam':
        dbexports_maps.map(dbpath='hubs.db', out=out, max_age=max_age)
    

@fc_nmap.command()
@click.option('--out', default='fc_nmap.html', help="Output file")
@click.option('--max-age', default=86400, help="Only check records that were created/updated in the last INTEGER seconds.", show_default=True)
def map(out, max_age):
    dbexports_maps.create_map(dbpath='hubs.db', out=out, max_age=max_age)
    
    