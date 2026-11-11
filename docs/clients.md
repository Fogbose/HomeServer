# Windows, Android and iOS clients

Replace `https://cloud.example.org` with your own private HTTPS origin. Each
person needs their own Nextcloud account and the required shares. Connect to
your authorized private network first (for example Tailscale). Do not expose
Nextcloud publicly just to connect a phone, and do not bypass certificate errors.
Private shared Forms links still require network access.

Every selected app has a web interface on all three platforms. Native clients
are optional, differ in features and may cost money. No purchase or third-party
installer is bundled here. Do not assume a widget or offline mode exists for
every app. See the current official client lists before installing.

## Windows

Install [Tailscale](https://tailscale.com/download) if used by your deployment,
[Nextcloud Desktop](https://nextcloud.com/install/) for files and
[Thunderbird](https://www.thunderbird.net/) for calendars, tasks and contacts.
Existing installations should be reused. With WinGet, these are the package IDs
to review: `Tailscale.Tailscale`, `Nextcloud.NextcloudDesktop`,
`Mozilla.Thunderbird`. Normal installers may require your Windows consent.

Connect Desktop to `https://cloud.example.org` through its browser login. Choose
virtual files or local folders deliberately. The file client does not synchronize
all App Store apps; use their web interfaces for Cookbook, Cospend, Tables,
Forms, Deck, Notes and Memories.

Thunderbird does not need a mail account for DAV. Cancel the initial email/full
name wizard. Create a **network calendar** with your Nextcloud username and
`https://cloud.example.org/remote.php/dav`. Leave **This location doesn't require
credentials** unchecked. **Offline Support** can stay checked on a trusted PC;
it stores a local copy. Select the calendars/task lists discovered. Separately
add a **CardDAV address book** using the same server and username. Use an app
password when required by two-factor authentication; never paste it into this
repository or a support issue. Test creation and edits in both directions.

## Android

Use Nextcloud for file/photo uploads. For calendars/contacts/tasks,
[DAVx5](https://www.davx5.com/tested-with/nextcloud) provides DAV synchronization;
check its [distribution options](https://www.davx5.com/download/) and pricing.
Use [Tasks.org](https://tasks.org/) through DAVx5 for tasks, rather than adding
the same task account a second time through direct CalDAV. Select the desired
calendars/books and allow background synchronization as needed.

Start with web interfaces for the remaining apps. Optional native clients are
listed by [Notes](https://github.com/nextcloud/notes/wiki),
[Deck](https://github.com/nextcloud/deck#mobile-apps),
[Memories](https://memories.gallery/) and
[Cookbook](https://github.com/nextcloud/cookbook). For Cospend the web interface
avoids relying on older unmaintained mobile clients.

## iOS / iPadOS

Use Nextcloud for files and a single photo-upload pipeline. In Settings, add a
CalDAV account for calendars and a separate CardDAV account for contacts using
your HTTPS server and Nextcloud username. If discovery requires it, obtain the
principal URL from Nextcloud; its usual form is
`https://cloud.example.org/remote.php/dav/principals/users/YOUR_USERNAME/`.
URL-encode the real username; keep SSL enabled. Use the task web interface first;
do not assume Apple Reminders preserves all CalDAV recurrence behavior.

Use Safari for Cospend, Cookbook, Deck, Notes, Memories, Tables and Forms; a Home
Screen shortcut gives quick access. Native alternatives may have narrower
features. iOS background restrictions can delay automatic file/photo uploads.

## Passwords and first-use validation

[Passwords](https://passwordsapp.org/) is a community project. Follow its current
client/extension links, verify the publisher and test encryption compatibility
and recovery before importing a password collection. Keep recovery material
offline. Apple Passwords and a Nextcloud Passwords client are separate products.

For each person test: file upload/download, event and contact two-way changes,
recurring-task completion and next occurrence, a shared recipe, an expense and
balance, a board change, a form response and a small photo/video. Check shares
with a non-admin account. Browser access alone does not prove background sync.
No API key or paid AI service is needed for this setup.

Sources: [Thunderbird synchronization](https://docs.nextcloud.com/server/stable/user_manual/en/groupware/sync_thunderbird.html),
[iOS synchronization](https://docs.nextcloud.com/server/stable/user_manual/en/groupware/sync_ios.html),
[Nextcloud clients](https://nextcloud.com/install/).
