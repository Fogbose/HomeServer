# Optional Nextcloud App Store applications

These are extensions inside the existing Nextcloud application, not eleven new
Docker services. They share its authentication, database, files, cron and backup
lifecycle. The base stack remains usable without them. No custom household app,
fairness allocator, automatic task assignment or points system is shipped here.

The selected catalogue is in [applications/catalogue.json](../applications/catalogue.json).
Its `observed_version` values record a reported Nextcloud 34.0.5 / PHP 8.5.12
installation on 2026-11-09; they are not download pins or compatibility guarantees.
Use the installed server's App Store compatibility checks at installation time.

| App ID | Use | Avoid overlapping workflows |
| --- | --- | --- |
| cookbook | Shared recipes | Start with the web interface |
| cospend | Shared expenses and balances | Share each project explicitly |
| calendar | Events and shared calendars | One DAV account per client |
| contacts | Shared/personal address books | Select the books to synchronize |
| tasks | Daily and recurring tasks | Test recurrence with your chosen client |
| notes | Personal notes | Keep structured records in Tables |
| passwords | Community password manager | Test recovery and client compatibility first |
| memories | Photo/video timeline | One automatic upload pipeline |
| tables | Structured lists | Use Forms to collect submissions |
| forms | Questionnaires | Private access still applies to shared links |
| deck | Project boards | Use Tasks for daily checklists |

News, Music and Polls are deferred. Mail, a mail server and chat are outside this
selection. Keeping Photos enabled is useful for Memories album support.

## Installation on Linux

First review [backup and isolated recovery](backup-restore.md), capture a coherent
backup and verify a restore. Test on disposable data before using a live server.
App installation changes the database; disabling an app does not undo migrations.
Do not import private backups into a public CI job.

From the directory containing `compose.yaml`, inspect the baseline:

```sh
docker compose exec -T -u www-data app php occ status
docker compose exec -T -u www-data app php occ app:list --output=json
```

In Nextcloud, use **Administration → Apps** to select compatible stable releases.
Alternatively repeat the following for each chosen ID from the table, replacing
`cookbook`. Install only missing apps; for an already installed app check its
version/integrity and enable it without implicitly upgrading it:

```sh
docker compose exec -T -u www-data app php occ app:install --keep-disabled cookbook
docker compose exec -T -u www-data app php occ integrity:check-app cookbook
docker compose exec -T -u www-data app php occ app:enable cookbook
docker compose exec -T -u www-data app php occ app:list --output=json
```

Stop if any command fails; investigate before proceeding. Never use `--force`,
unstable releases or `app_install_overwrite` to bypass compatibility. The native
installer resolves compatibility and verifies packages. Raw App Store platform
JSON can differ from the server's filtered metadata; it is not a substitute.
Disabled entries in `app:list` can contain `VERSION (installed VERSION)`;
do not compare that entire display string with a bare version.

For Memories, continue with the [persistent media image](memories.md). After
installation configure cron, check maintenance/upgrade state, sign in with a
daily account and test each app with disposable records. Share calendars,
address books, boards, recipes and expense projects deliberately; installing an
app alone does not create family permissions.

## Updates and recovery

Record installed versions and review each app's compatibility before a core
upgrade. The catalogue is not an automatic updater. If an app fails, preserve
logs privately, disable only that app if appropriate and assess the failure.
Reverting container images alone cannot reverse database changes; a coherent
restore requires the matching files/configuration/database and a tested plan.

Sources: [Nextcloud App Store](https://apps.nextcloud.com/),
[OCC administration](https://docs.nextcloud.com/server/stable/admin_manual/occ_command.html),
[Memories configuration](https://memories.gallery/config/),
[Passwords project](https://passwordsapp.org/).
