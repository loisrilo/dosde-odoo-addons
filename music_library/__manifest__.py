# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Music Library",
    "summary": "Manage music files",
    "version": "15.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://github.com/loisrilo/",
    "author": "Lois Rilo",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/music_library_security.xml",
        "security/ir.model.access.csv",
        "views/music_track_view.xml",
        "views/music_album_views.xml",
        "views/music_artist_views.xml",
        "views/music_genre_views.xml",
    ],
}
