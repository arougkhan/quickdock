'use strict';

//var service = require('persistence.js')
import express from 'express';
import * as persistence from "./persistence"
import {baseMapColl, userMapColl} from "./persistence";

const app = express();
app.use(express.json());

// Monitoring and troubleshooting
app.get('/ping', (req, res) => {
    console.log("Got ping");
    res.send('keymap service: pong (Node/Express)');
});
app.get('/auth/me', function (req, res) {
    res.send('TODO: show JWT user info here');
})

// Return combined keymap for logged in user
app.get('/keymap/composite-map/:keymap_alias', async function (req, res) {
    let reply = await combineMaps("test_user", "test_org", req.params["keymap_alias"])
    res.send(reply);
})
app.get('/keymap/composite-map/', async function (req, res) {
    let reply = await combineMaps("test_user", "test_org", "default")
    res.send(reply);
})

async function combineMaps(userId:String, orgId:String, mapName:String) {
    let userMapper = await persistence.getKeymap(userId, mapName, userMapColl)
    let baseMapper = await persistence.getKeymap(orgId, mapName, baseMapColl)
    let keyMap = new Map()
    baseMapper['keymap'].forEach((element:any) => keyMap.set(element['key'],element['value']))
    userMapper['keymap'].forEach((element:any) => keyMap.set(element['key'],element['value']))
    return Array.from(keyMap, ([name, value]) => ({'key': name, 'value': value}))
}

// ** User keymaps **
// Get all maps for user
app.get('/keymap/user-maps', async function (req, res) {
    res.send(await persistence.getKeymaps("test_user", userMapColl));
})
// Access named user map
app.get('/keymap/user-map/:keymap_alias',async function (req, res) {
    res.send(await persistence.getKeymap("test_user", req.params["keymap_alias"], userMapColl));
})
app.put('/keymap/user-map/:keymap_alias', async function (req, res) {
    res.send(await persistence.storeKeymap("test_user", req.params["keymap_alias"], req.body, userMapColl));
})
app.delete('/keymap/user-map/:keymap_alias', async function (req, res) {
    res.send(await persistence.deleteKeymap("test_user", req.params["keymap_alias"], userMapColl));
})
app.post('/keymap/user-map', async function (req, res) {
    if ('keymap_alias' in req.body) {
        res.send(await persistence.storeKeymap("test_user", req.body['keymap_alias'], req.body, userMapColl))
    } else
        res.send(await persistence.storeKeymap("test_user", 'default', req.body, userMapColl))
})

// Access individual entries in named user-map
app.get('/keymap/user-map/:keymap_alias/items/:item_key', async function (req, res) {
        let current = await persistence.getKeymap("test_user", req.params["keymap_alias"], userMapColl)
        res.status(200).send(JSON.stringify(current['keymap'].find((entry:any) => entry['key'] == req.params['item_key'])));
})
app.put('/keymap/user-map/:keymap_alias/items/:item_key', async function (req, res) {
        let current = await persistence.getKeymap("test_user", req.params["keymap_alias"], userMapColl)
        current['keymap'] = upsertEntry(req.params['item_key'], req.body['value'], current['keymap'])
        await persistence.storeKeymap("test_user", req.params["keymap_alias"], current, userMapColl)
        res.status(201).send('Keymap updated');
})
app.post('/keymap/user-map/:keymap_alias/items', async function (req, res) {
    let current = await persistence.getKeymap("test_user", req.params["keymap_alias"], userMapColl)
    current['keymap'] = upsertEntry(req.body['key'], req.body['value'], current['keymap'])
    await persistence.storeKeymap("test_user", req.params["keymap_alias"], current, userMapColl)
    res.status(201).send('Keymap updated');
})
app.delete('/keymap/user-map/:keymap_alias/items/:item_key', async function (req, res) {
    let current = await persistence.getKeymap("test_user", req.params["keymap_alias"], userMapColl)
    current['keymap'] = removeEntry(req.body['key'], req.body['value'], current['keymap'])
    await persistence.storeKeymap("test_user", req.params["keymap_alias"], current, userMapColl)
    res.status(201).send('Entry removed from keymap');
})


// ** Base keymaps **
// Get all base maps
app.get('/keymap/base-maps', async function (req, res) {
    res.send(await persistence.getKeymaps("test_org", baseMapColl));
})
// Access named user map
app.get('/keymap/base-map/:keymap_alias',async function (req, res) {
    res.send(await persistence.getKeymap("test_org", req.params["keymap_alias"], baseMapColl));
})
app.put('/keymap/base-map/:keymap_alias', async function (req, res) {
    res.send(await persistence.storeKeymap("test_org", req.params["keymap_alias"], req.body, baseMapColl));
})
app.delete('/keymap/base-map/:keymap_alias', async function (req, res) {
    res.send(await persistence.deleteKeymap("test_org", req.params["keymap_alias"], baseMapColl));
})
app.post('/keymap/base-map', async function (req, res) {
    if ('keymap_alias' in req.body) {
        res.send(await persistence.storeKeymap("test_org", req.body['keymap_alias'], req.body, baseMapColl))
    } else
        res.send(await persistence.storeKeymap("test_org", 'default', req.body, baseMapColl))
})

// Access individual entries in named user-map
app.get('/keymap/base-map/:keymap_alias/items/:item_key', async function (req, res) {
    let current = await persistence.getKeymap("test_org", req.params["keymap_alias"], baseMapColl)
    res.status(200).send(JSON.stringify(current['keymap'].find((entry:any) => entry['key'] == req.params['item_key'])));
})
app.put('/keymap/base-map/:keymap_alias/items/:item_key', async function (req, res) {
    let current = await persistence.getKeymap("test_org", req.params["keymap_alias"], baseMapColl)
    current['keymap'] = upsertEntry(req.params['item_key'], req.body['value'], current['keymap'])
    await persistence.storeKeymap("test_org", req.params["keymap_alias"], current, baseMapColl)
    res.status(201).send('Keymap updated');
})
app.post('/keymap/base-map/:keymap_alias/items', async function (req, res) {
    let current = await persistence.getKeymap("test_org", req.params["keymap_alias"], baseMapColl)
    current['keymap'] = upsertEntry(req.body['key'], req.body['value'], current['keymap'])
    await persistence.storeKeymap("test_org", req.params["keymap_alias"], current, baseMapColl)
    res.status(201).send('Keymap updated');
})
app.delete('/keymap/base-map/:keymap_alias/items/:item_key', async function (req, res) {
    let current = await persistence.getKeymap("test_org", req.params["keymap_alias"], baseMapColl)
    current['keymap'] = removeEntry(req.body['key'], req.body['value'], current['keymap'])
    await persistence.storeKeymap("test_org", req.params["keymap_alias"], current, baseMapColl)
    res.status(201).send('Entry removed from keymap');
})

// Utility: Insert or replace item in keymap
function upsertEntry(itemKey: String, itemValue: String, keymap: any) {
    let updatedKeymap = removeEntry(itemKey, itemValue, keymap)
    updatedKeymap.push({key: itemKey, value: itemValue})
    return updatedKeymap
}
function removeEntry(itemKey: String, itemValue: String, keymap: any) {
    return keymap.filter(function(obj: any) { return obj['key'] !== itemKey})
}

// Run as standalone app
const PORT = 5001;
const HOST = '0.0.0.0';

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);