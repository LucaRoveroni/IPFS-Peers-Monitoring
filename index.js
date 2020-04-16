// Required modules
const superagent = require('superagent');
const geoip = require('geoip-lite');
const fs = require('fs');

// Invoke IPFS Daemon APIs
async function readSwarm() {
    const ipfs_path = 'http://127.0.0.1:5001/api/v0/swarm/peers?latency=true';
    console.log('Data: ' + new Date().toISOString());
    try {
        const req = await superagent.post(ipfs_path);
        if (!req.body.hasOwnProperty('Peers')) {
            console.log('At the moment there aren\'t any peers');
        } else {
            req.body.Peers.forEach(peer => {
                // Add new informations per peer
                const peer_ip = peer['Addr'].split('/')[2];
                if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(peer_ip)) {
                    const geo = geoip.lookup(peer_ip);
                    // console.log(geo)
                    // console.log(peer)
                    peer['Country'] = geo.country;
                    peer['City'] = geo.city;
                    peer['Timestamp'] = new Date().toISOString();
                    peer['IPv4'] = peer_ip;

                    // Delete some useless data
                    delete peer['Addr']
                    delete peer['Streams']
                    delete peer['Direction']
                    delete peer['Muxer']
                }
            });

            fs.readFile('swarm_monitor2.json', (err, data) => {
                var json = JSON.parse(data);
                var newArray = json.Peers.concat(req.body.Peers);
                var output = {
                    "Peers": newArray
                }
                fs.writeFile('swarm_monitor2.json', JSON.stringify(output), 'utf8', cb => {
                    console.log('Written on file!');
                })
            })
        }
    } catch (err) {
        console.error(err);
    }
}

async function main() {
    // Recall the function every hour
    readSwarm();
    setInterval(readSwarm, 1000 * 60 * 60);
}

// Start main program
main();