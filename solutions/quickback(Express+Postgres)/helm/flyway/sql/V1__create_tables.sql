create EXTENSION if not exists "uuid-ossp";
create table if not exists custom_maps
(
    id              uuid  default uuid_generate_v4() not null
        constraint custom_maps_pkey
            primary key,
    user_id         varchar,
    keymap_alias    varchar,
    keymap         jsonb default '[]'::jsonb
);
create unique index if not exists idx_custom_maps on custom_maps(user_id, keymap_alias);
create table if not exists base_maps
(
    id              uuid  default uuid_generate_v4() not null
        constraint base_maps_pkey
            primary key,
    user_id         varchar,
    keymap_alias    varchar,
    keymap         jsonb default '[]'::jsonb
);
create unique index if not exists idx_base_maps on base_maps(user_id, keymap_alias);

INSERT INTO base_maps (id, user_id, keymap_alias, keymap)
VALUES (DEFAULT, 'test_org', 'default', '[{"key": "phrase_A", "value": "A from base map expanded!"}, {"key": "phrase_B",
  "value": "B from base map expanded!"}, {"key": "phrase_C", "value": "C from base map expanded!"}]');

INSERT INTO custom_maps (id, user_id, keymap_alias, keymap)
VALUES (DEFAULT, 'test_user', 'default', '[{"key": "phrase_A", "value": "A from user map expanded!"}, {"key": "phrase_B",
  "value": "B from base map expanded!"}, {"key": "phrase_D", "value": "D from user map expanded!"}]');