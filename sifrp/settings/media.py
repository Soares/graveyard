from environment import PROJECT_ROOT, PROJECT_NAME

MEDIA_ROOT = PROJECT_ROOT + '/static/'
MEDIA_URL = '/static/'

MEDIA_BUNDLES = (
    # ---------------------------------- CSS
    # Core
    ('core.css',
        'tools/reset/reset.css',
        'tools/reset/scaffold.css',
        'tools/jquery/ui/css/hot-sneaks/theme.css',
        'main/sass/roller.sass',
        'main/sass/core.sass',
    ),
    ('base.css', 'main/sass/base.sass'),
    ('full.css', 'main/sass/full.sass'),

    # Main Pages
    ('welcome.css', 'main/sass/welcome.sass'),

    # Accounts
    ('profile.css', 'accounts/sass/profile.sass'),

    # Character
    ('character.css',
        'characters/sass/character.sass',
        'characters/sass/menu.sass',
        'characters/sass/left.sass',
        'characters/sass/panes.sass',
        'characters/sass/abilities.sass',
        'characters/sass/qualities.sass',
        'characters/sass/dialogs.sass',
    ),

    # ---------------------------------- JS
    # Core
    ('top.js', 'tools/modernizr/1.6.min.js'),
    ('core.js',
        'tools/jquery/1.6.1.min.js',
        'tools/jquery/ui/1.8.13.min.js',
        'tools/underscore/1.1.6.min.js',
        'tools/backbone/0.5.1.min.js',
        'utility/js/storage.js',
        'utility/js/string.js',
        'utility/coffee/confirm.coffee',
        'main/coffee/roller.coffee',
        'main/js/core.js',
    ),
    ('form.js',
        'tools/jquery/validate/1.8.1.min.js',
        'tools/jquery/form.js',
    ),
    ('app.js',
        'tools/jquery/tmpl/1.0pre.min.js',
        'tools/backbone/localstorage.js',
        'tools/backbone/forms.coffee',
        'tools/backbone/family.coffee',
    ),

    # Main Pages
    ('welcome.js', 'main/js/welcome.js'),

    # Accounts
    ('profile.js', 'accounts/js/profile.js'),

    # Westeros
    ('westeros.js',
        'westeros/rulebook.js',

        'westeros/fixtures/abilities.js',
        'westeros/fixtures/ages.js',
        'westeros/fixtures/armor.js',
        'westeros/fixtures/qualities.coffee',
        'westeros/fixtures/benefits.coffee',
        'westeros/fixtures/drawbacks.coffee',
        'westeros/fixtures/items.js',
        'westeros/fixtures/money.js',
        'westeros/fixtures/mounts.js',
        'westeros/fixtures/prices.js',
        'westeros/fixtures/weapons.js',
    ),

    # Character
    ('character.js',
        # Routing
        'characters/coffee/router.coffee',

        # Independant Models
        'characters/coffee/models/models.coffee',
        'characters/coffee/models/abilities.coffee',
        'characters/coffee/models/age.coffee',
        'characters/coffee/models/log.coffee',
        'characters/coffee/models/money.coffee',
        'characters/coffee/models/qualities.coffee',
        'characters/coffee/models/item.coffee',
            'characters/coffee/models/armor.coffee',
            'characters/coffee/models/mount.coffee',
            'characters/coffee/models/weapon.coffee',
        'characters/coffee/models/character.coffee',

        # Initialization
        'characters/coffee/character.coffee',

        # Actions
        'characters/coffee/actions/actions.coffee',
        'characters/coffee/actions/pool.coffee',
            'characters/coffee/actions/attack.coffee',

        # Data linking
        'characters/coffee/links/links.coffee',
        'characters/coffee/links/experience.coffee',
        'characters/coffee/links/age.coffee',

        # Views
        'characters/coffee/views/views.coffee',
            # Rulebook references
            'characters/coffee/views/reference/reference.coffee',
            'characters/coffee/views/reference/qualities.coffee',
            'characters/coffee/views/reference/age.coffee',
            # Views that run in the background
            'characters/coffee/views/background/background.coffee',
            'characters/coffee/views/background/character.coffee',
            # Menu views
            'characters/coffee/views/menu/menu.coffee',
            'characters/coffee/views/menu/clone.coffee',
            'characters/coffee/views/menu/download.coffee',
            'characters/coffee/views/menu/new.coffee',
            'characters/coffee/views/menu/open.coffee',
            'characters/coffee/views/menu/remove.coffee',
            'characters/coffee/views/menu/reset.coffee',
            'characters/coffee/views/menu/settings.coffee',
            # Compact modules
            'characters/coffee/views/modules/modules.coffee',
            'characters/coffee/views/modules/age.coffee',
            'characters/coffee/views/modules/control.coffee',
            'characters/coffee/views/modules/destiny.coffee',
            'characters/coffee/views/modules/experience.coffee',
            'characters/coffee/views/modules/gender.coffee',
            'characters/coffee/views/modules/glory.coffee',
            'characters/coffee/views/modules/house.coffee',
            'characters/coffee/views/modules/personality.coffee',
            # Character panes
            'characters/coffee/views/panes/panes.coffee',
            'characters/coffee/views/panes/abilities.coffee',
            'characters/coffee/views/panes/logs.coffee',
            'characters/coffee/views/panes/notes.coffee',
            'characters/coffee/views/panes/qualities.coffee',
    ),
)
