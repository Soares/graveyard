/**
 * editor_plugin_src.js
 *
 * Copyright 2009, Moxiecode Systems AB
 * Released under LGPL License.
 *
 * License: http://tinymce.moxiecode.com/license
 * Contributing: http://tinymce.moxiecode.com/contributing
 */

(function() {
    // 'abcdefghijklmnopqrstuvwxyz'
    var lowercase = 'αβχδεϝγηιςκλμνθπϙρστυφωξψζ';
    var uppercase = 'ΑΒΧΔΕFΓͰΙⱶΚΛΜΝΘΠϘΡΣΤΥΦΩΞΨΖ';
	// Load plugin specific language pack
	tinymce.PluginManager.requireLangPack('greek');

	tinymce.create('tinymce.plugins.GreekPlugin', {
		/**
		 * Initializes the plugin, this will be executed after the plugin has been created.
		 * This call is done before the editor instance has finished it's initialization so use the onInit event
		 * of the editor instance to intercept that event.
		 *
		 * @param {tinymce.Editor} ed Editor instance that the plugin is initialized in.
		 * @param {string} url Absolute URL to where the plugin is located.
		 */
		init : function(ed, url) {
			// Register the command so that it can be invoked by using tinyMCE.activeEditor.execCommand('mceGreek');
            ed.greek = false;
			ed.addCommand('mceGreek', function() {
                ed.greek = true;
			});

			// Register greek button
			ed.addButton('greek', {
				title : 'greek.desc',
				cmd : 'mceGreek',
				image : url + '/img/greek.gif'
			});

            ed.onKeyPress.add(function(ed, e) {
                if(ed.greek) {
                    if(e.which >= 65 && e.which <= 90) {
                        ed.execCommand('mceInsertContent',false,uppercase[e.which-65]);
                        e.preventDefault();
                    } else if(e.which >= 97 && e.which <= 122) {
                        ed.execCommand('mceInsertContent',false,lowercase[e.which-97]);
                        e.preventDefault();
                    }
                }
                ed.greek = false;
            });

            ed.addShortcut('ctrl+g', 'lang_greek_desc', 'mceGreek');
            /*
			// Add a node change handler, selects the button in the UI when a image is selected
			ed.onNodeChange.add(function(ed, cm, n) {
				cm.setActive('greek', n.nodeName == 'IMG');
			});
            */
		},

		/**
		 * Creates control instances based in the incomming name. This method is normally not
		 * needed since the addButton method of the tinymce.Editor class is a more easy way of adding buttons
		 * but you sometimes need to create more complex controls like listboxes, split buttons etc then this
		 * method can be used to create those.
		 *
		 * @param {String} n Name of the control to create.
		 * @param {tinymce.ControlManager} cm Control manager to use inorder to create new control.
		 * @return {tinymce.ui.Control} New control instance or null if no control was created.
		 */
		createControl : function(n, cm) {
			return null;
		},

		/**
		 * Returns information about the plugin as a name/value array.
		 * The current keys are longname, author, authorurl, infourl and version.
		 *
		 * @return {Object} Name/value array containing information about the plugin.
		 */
		getInfo : function() {
			return {
				longname : 'Greek plugin',
				author : 'Some author',
				authorurl : 'http://tinymce.moxiecode.com',
				infourl : 'http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/greek',
				version : "1.0"
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('greek', tinymce.plugins.GreekPlugin);
})();
