# WTF

- What is `treq`?
- Why have `mutables_bad` on 178
- What's the tahoe welcome page?
- glossary:
  - entry_cap
  - mutable_cap
  - path_name
- L193 Create Immutable DIRECTORY !? Why immutable, does that mean we can't add items to it?
- L320 `directory_data` vs `list_directory` ?  Why would we want the raw data?

## Decisions:

- Local Docker deployment: Should we:
  - Create client config (inside the container) with every run
  - Create (persistent) client config outside container?
  - Check for existing config, then create (persistent) client config outside container?