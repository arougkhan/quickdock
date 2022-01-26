const Pool = require('pg').Pool
const pool = new Pool({
    user: 'postgres',
    host: 'node_db',
    database: 'keymap',
    password: 'password',
    port: 5432,
})

const userMapColl = "custom_maps"
const baseMapColl = "base_maps"

 // SQL factory functions
function GET_KEYMAP(collection: String, userId: String, keymapAlias: String) {
    return "SELECT keymap_alias, keymap FROM " + collection +
        " WHERE user_id = '" + userId + "' AND keymap_alias = '" + keymapAlias + "'";
}
function GET_KEYMAP_WITH_UID(collection: String, userId: String, keymapAlias: String) {
    return "SELECT user_id, keymap_alias, keymap FROM " + collection +
        " WHERE user_id = '" + userId + "' AND keymap_alias = '" + keymapAlias + "'";
}
function GET_KEYMAPS(collection: String, userId: String) {
    return "SELECT keymap_alias FROM " + collection + " WHERE user_id = '" + userId + "'";
}
function DELETE_KEYMAP(collection: String, userId: String, keymapAlias: String) {
    return "DELETE FROM " + collection + " WHERE user_id = '" + userId + "' AND keymap_alias = '" + keymapAlias + "'";
}
function INSERT_OR_UPDATE_KEYMAP(collection: String, userId: String, keymapAlias: String, keymapValue: any) {
    return "INSERT INTO " + collection + " (user_id, keymap_alias, keymap) VALUES('" + userId + "','" + keymapAlias + "','" + keymapValue + "') " +
        "ON CONFLICT(user_id, keymap_alias) DO UPDATE SET keymap = '" + keymapValue + "'";
}

const allRows = (a: any): any => {return a}
const firstRow = (a: any): any => {return a[0]}


async function runQuery(sql: String, callbackFormat: (a: any) => any = firstRow) {
    try {
        const res = await pool.query(sql);
        return callbackFormat(res.rows);
    } catch (err){
        return err;
    }
}

async function getKeymapWithUid(user_id: String, keymap_alias: String, collection: String) {
    console.log(GET_KEYMAP(collection, user_id, keymap_alias));
    const result = await runQuery(GET_KEYMAP_WITH_UID(collection, user_id, keymap_alias));
    console.log(result);
    return result;
}

async function getKeymap(user_id: String, keymap_alias: String, collection: String) {
    console.log(GET_KEYMAP(collection, user_id, keymap_alias));
    const result = await runQuery(GET_KEYMAP(collection, user_id, keymap_alias));
    console.log(result);
    return result;
}

async function storeKeymap(user_id: String, keymap_alias: String, keymapper: any, collection: String) {
    const result = await runQuery(INSERT_OR_UPDATE_KEYMAP(collection, user_id, keymap_alias, JSON.stringify(keymapper["keymap"])));
    return result;
}

async function deleteKeymap(user_id: String, keymap_alias: String, collection: String) {
    console.log(DELETE_KEYMAP(collection, user_id, keymap_alias))
    const result = await runQuery(DELETE_KEYMAP(collection, user_id, keymap_alias));
    console.log(result);
    return result;
}

async function getKeymaps(user_id: String, collection: String) {
    console.log(GET_KEYMAPS(collection, user_id));
    const result = await runQuery(GET_KEYMAPS(collection, user_id), allRows);
    console.log(result);
    return result;
}

export {getKeymaps, getKeymap, getKeymapWithUid, storeKeymap, deleteKeymap, userMapColl, baseMapColl}
