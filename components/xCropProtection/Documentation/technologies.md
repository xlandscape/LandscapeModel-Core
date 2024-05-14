Work in progress

# Technologies.xml

Technologies include a name and a drift reduction factor, which is the factor by which spray-drift is reduced by technological measures. A Technology.xml file describes one or more technologies.

## Elements

### Technology Name

The name of the technology which may include spaces.

### Drift Reduction

A value between 0 and 1 that represents the percent by which spray-drift is reduced when using this technology. This value is a constant number and does not support random values.

## Examples

A Technology.xml file with 1 technology

    <Technologies xmlns="urn:xCropProtectionLandscapeScenarioParametrization">
        <Technology>
            <TechnologyName scales="global">Technology</TechnologyName>
            <DriftReduction type="float" unit="1" scales="global">0.5</DriftReduction>
        </Technology>
    </Technologies>

A Technology.xml file with 2 technologies

    <Technologies xmlns="urn:xCropProtectionLandscapeScenarioParametrization">
        <Technology>
            <TechnologyName scales="global">Technology</TechnologyName>
            <DriftReduction type="float" unit="1" scales="global">0.5</DriftReduction>
        </Technology>
        <Technology>
            <TechnologyName scales="global">Technology 2</TechnologyName>
            <DriftReduction type="float" unit="1" scales="global">0.3</DriftReduction>
        </Technology>
    </Technologies>
