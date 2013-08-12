import unittest

from overviewer import configParser
from overviewer.settingsValidators import ValidationException

from overviewer import world
from overviewer import rendermodes

class SettingsTest(unittest.TestCase):
    
    def setUp(self):
        self.s = configParser.MultiWorldParser()
    
    def test_missing(self):
        "Validates that a non-existant settings.py causes an exception"
        self.assertRaises(ValueError, self.s.parse, "doesnotexist.py")

    def test_existing_file(self):
        self.s.parse("test/data/settings/settings_test_1.py")
        things = self.s.get_validated_config()
        # no exceptions so far.  that's a good thing

        # Test the default
        self.assertEquals(things['renders']['myworld']['bgcolor'], (26,26,26,0))

        # Test a non-default
        self.assertEquals(things['renders']['otherworld']['bgcolor'], (255,255,255,0))

        self.assertEquals(things['renders']['myworld']['northdirection'],
               world.UPPER_LEFT) 

    def test_rendermode_validation(self):
        self.s.parse("test/data/settings/settings_test_rendermode.py")

        self.assertRaises(ValidationException,self.s.get_validated_config)

    def test_manual(self):
        """Tests that manually setting the config parser works, you don't have
        to do it from a file
        
        """
        fromfile = configParser.MultiWorldParser()
        fromfile.parse("test/data/settings/settings_test_1.py")

        self.s.set_config_item("worlds", {
            'test': "test/data/settings/test_world",
            })
        self.s.set_config_item("renders", {
                "myworld": { 
                    "title": "myworld title",
                    "world": "test",
                    "rendermode": rendermodes.normal,
                    "northdirection": "upper-left",
                },

                "otherworld": {
                    "title": "otherworld title",
                    "world": "test",
                    "rendermode": rendermodes.normal,
                    "bgcolor": "#ffffff"
                },
            })
        self.s.set_config_item("outputdir", "/tmp/fictional/outputdir")
        self.assertEquals(fromfile.get_validated_config(), self.s.get_validated_config())

    def test_rendermode_string(self):
        self.s.set_config_item("worlds", {
            'test': "test/data/settings/test_world",
            })
        self.s.set_config_item("outputdir", "/tmp/fictional/outputdir")
        self.s.set_config_item("renders", {
                "myworld": { 
                    "title": "myworld title",
                    "world": "test",
                    "rendermode": "normal",
                    "northdirection": "upper-left",
                },
                })
        p = self.s.get_validated_config()
        self.assertEquals(p['renders']['myworld']['rendermode'], rendermodes.normal)

if __name__ == "__main__":
    unittest.main()
