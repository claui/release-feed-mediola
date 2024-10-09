<!-- markdownlint-configure-file { "MD041": { "level": 1 } } -->

# Synopsis

```shell
release-feed-mediola [PRODUCT]
```

# Description

To generate an Atom feed for a given Mediola product, run
`release-feed-mediola` with the product name as an argument.

To see a list of supported Mediola products, run
`release-feed-mediola` without arguments.

# Configuration

## Updating your feed automatically with systemd

You may want to run `release-feed-mediola` periodically to generate
and update a feed file using a systemd timer and service.
This requires a Linux system and systemd version 256 or newer.

## Installing the unit files

First, install the systemd timer and service unit files.

- If you have installed `release-feed-mediola` from a Debian package
  or from the AUR, the unit files have already been installed.

- Otherwise, download the unit files `release-feed-mediola@.service`
  and `release-feed-mediola@.timer` from the `contrib/systemd`
  directory on the GitHub repository. Place the files into your
  `/etc/systemd/user/` directory. You may have to edit the
  paths inside the `ExecStart` directive to match your Linux distro.

## Enabling the timer

To enable the systemd timer for a given Mediola product, run:

```shell
# Replace PRODUCT with the Mediola product name you want to track
systemctl --user enable --now release-feed-mediola@PRODUCT.timer
```

You can enable and run multiple timers for different Mediola
products at the same time.

Each service will generate one `feed.atom` file per product once a
day.

## Setting up your feed reader

For each product you want to track, locate the generated `feed.atom`
file in the `~/.local/share/feeds/release-feed-mediola/` directory
hierarchy. Point your feed reader software to that file.

You may want to use a `file:///` URL if your reader doesn’t support
feeds from the local filesystem directly. For example:

> `file:///home/yourusername/.local/share/feeds/release-feed-mediola/neo/feed.atom`

## Disabling the timer

To disable the systemd timer for a given Mediola product, run:

```shell
# Replace PRODUCT with the Mediola product name you want to track
systemctl --user disable --now release-feed-mediola@PRODUCT.timer
```

# Environment

release-feed-mediola supports the following environment variable:

`RELEASE_FEED_MEDIOLA_DEBUG`
: If set to a non-zero value, causes release-feed-mediola to enable debug-level
: logging.
: Also prints stack traces for errors where it normally would not.
