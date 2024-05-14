# xCropProtection.xml

The purpose of xCropProtection.xml is to specify all user-created files that should be used in an xCP scenario.

## Elements

### PPM Calendars

1 or more PPM Calendars to be included in the scenario. xCP will use both calendars when running the scenario, and only apply a calendar when the crop type/field ID is appropriate. Separate PPM Calendars must be created when different application regimes are necessary (e.g. different set of products applied to different crops)

### Technologies

1 Technologies.xml file which includes all technology options for the scenario.

## Examples

An xCropProtection.xml file.

    <XPPP xmlns="urn:xCropProtectionLandscapeScenarioParametrization" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:xCropProtectionLandscapeScenarioParametrization ../../../model/core/components/xCropProtection/xCropProtection.xsd">
        <PPMCalendars>
            <PPMCalendar include="PPMCalendar_1.xml"/>
            <PPMCalendar include="PPMCalendar_2.xml"/>
        </PPMCalendars>
        <Technologies include="Technologies.xml"/>
    </XPPP>