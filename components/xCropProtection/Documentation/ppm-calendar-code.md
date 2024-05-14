Work in progress

## PPM Calendar Technical Details

## Temporal Validity

**Type**: none, list[xCropProtection.MonthDaySpan], or list[xCropProtection.DateSpan]

**Unit**: N/A

**Scales**: time/simulation|time/day|time/year

**Notes**:
- Format: 'mm-dd to mm-dd' or 'yyyy-mm-dd to yyyy-mm-dd'.
- Set 'always' if the PPM Calendar should be applied over the whole simulation.
</ul>

Apply calendar over the whole simulation:

    <TemporalValidity scales="time/simulation">always</TemporalValidity>

Apply calendar over specific months each year:

    <TemporalValidity type="xCropProtection.MonthDaySpan">
        01-01 to 06-30
    </TemporalValidity>

Apply calendar only on specific years:

    <TemporalValidity type="xCropProtection.DateSpan">
        2001-01-01 to 2001-12-31
    </TemporalValidity>

## Target Crops

**Type**: int or list[int]

**Unit**: N/A

**Scales**: global|time/day|time/year

**Notes**:
- Separate target crops with a space.
</ul>

Apply PPM calendar to fields with crop type 9:

    <TargetCrops type="list[int]" scales="global">
        9
    </TargetCrops>

Apply PPM calendar to fields with crop type 9 or 16:

    <TargetCrops type="list[int]" scales="global">
        9 16
    </TargetCrops>

## Target Fields

**Type**: int or list[int]

**Unit**: N/A

**Scales**: global|time/day|time/year

**Notes**:
- Separate target fields with a space.
- The name of the identifier which uniquely identifies each field can be changed in package.xinfo located in the geo folder.
</ul>

Only apply PPM Calendar to field 100:

    <TargetFields type="list[int]" scales="global">
        100
    </TargetFields>

Only apply PPM Calendar to fields 30 and 31:

    <TargetFields type="list[int]" scales="global">
        30 31
    </TargetFields>

## Indications

**Type**: N/A or xCropProtection.ChoiceDistribution

**Unit**: N/A

**Scales**: time/year, space/base_geometry

**Notes**:
- If the type of this element is left blank, xCP will check all indications. If the type of this element is "xCropProtection.ChoiceDistribution", xCP will select one indication based on specified probability values.
</ul>

Use all indications:

    <Indications>
        <Indication>
            ...
        </Indication>
        <Indication>
            ...
        </Indication>
    <Indications>

Choose 1 indication based on probability values:

    <Indications type="xCropProtection.ChoiceDistribution" scales="time/year, space/base_geometry">
        <Indication probability="0.6">
            ...
        </Indication>
        <Indication probability="0.4">
            ...
        </Indication>
    <Indications>

## Indication

**Type**: xCropProtection.ChoiceDistribution

**Unit**: N/A

**Scales**: time/year, space/base_geometry

Choose 1 application sequence based on probability values:

    <Indication type="xCropProtection.ChoiceDistribution" scales="time/year, space/base_geometry">
        <ApplicationSequence probability="0.5">
            ...
        </ApplicationSequence>
        <ApplicationSequence probability="0.5">
            ...
        </ApplicationSequence>
    </Indication>

## Application Sequence

**Type**: N/A

**Unit**: N/A

**Scales**: N/A

**Notes**:
- Application sequence probabilities must sum to 1.0.
</ul>

Example of 1 Application Sequence:

    <ApplicationSequence probability="1">
        ...
    </ApplicationSequence>

Example of 2 Application Sequences:

    <ApplicationSequence probability="0.5">
        ...
    </ApplicationSequence>
    <ApplicationSequence probability="0.5">
        ...
    </ApplicationSequence>

## Application

**Type**: N/A

**Unit**: N/A

**Scales**: N/A

**Notes**:
- Each application in an application sequence will be applied to the selected field.
</ul>

    <Application>
        ...
    </Application>

## Tank

**Type**: N/A

**Unit**: N/A

**Scales**: N/A

**Notes**:
- If a tank mixture is being implemented (more than 1 product in the tank), the number of products in the tank must be the same as the number of application rates defined.

## Products

**Type**: list[str] (list of strings)

**Unit**: N/A

**Scales**: other/products

**Notes**:
- Multiple products must be separated with a | symbol. Products may have spaces in their names.
- The name specified in this element is what will be assigned to fields as they receive applications.
</ul>

    <Products type="list[str]" scales="other/products">
        Example Product
    </Products>

## Application Rates

**Type**: float, xCropProtection.NormalDistribution, or xCropProtection.UniformDistribution"

**Unit**: g/ha

**Scales**: global|time/day|time/year|time/day, space/base_geometry|time/year, space/base_geometry

Constant application rate:

    <ApplicationRate type="float" unit="g/ha" scales="global">300</ApplicationRate>

Uniform distribution application rate:

    <ApplicationRate type="xCropProtection.UniformDistribution" unit="g/ha" scales="time/year, space/base_geometry">
        <Lower type="float" scales="global">100</Lower>
        <Upper type="float" scales="global">150</Upper> 
    </ApplicationRate>

Normal distribution application rate:

    <ApplicationRate type="xCropProtection.NormalDistribution" unit="g/ha" scales="time/year, space/base_geometry">
        <Mean type="float" scales="global">50.0</Mean>
        <SD type="float" scales="global">4.0</SD> 
    </ApplicationRate>

## Application Window

**Type**: xCropProtection.MonthDaySpan

**Unit**: N/A

**Scales**: global

Notes:
- Format is Month-Day.
- Input must be in format "Month-Day to Month-Day".
</ul>

    <ApplicationWindow type="xCropProtection.MonthDaySpan" scales="global">05-05 to 05-16</ApplicationWindow>

## Technology

**Type**: string

**Unit**: N/A

**Scales**: global

Notes:
- This value must match a Technology element in Technologies.xml.
</ul>

    <Technology scales="global">Low-drift nozzle</Technology>

## In Crop Buffer

**Type**: float, xCropProtection.NormalDistribution, or xCropProtection.UniformDistribution

**Unit**: m (meter)

**Scales**: 
- Constant: global
- Normal/Uniform distribution: time/year, space/base_geometry|time/day, space/base_geometry

**Notes**: 
- A value less than 0 will not increase field size.
</ul>

Constant in crop buffer:

    <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>

In crop buffer with a uniform distribution:

    <InCropBuffer type="xCropProtection.UniformDistribution" unit="m" scales="time/year, space/base_geometry">
        <Lower type="float" scales="global">5</Lower>
        <Upper type="float" scales="global">10</Upper> 
    </InCropBuffer>

In crop buffer with a normal distribution:

    <InCropBuffer type="xCropProtection.NormalDistribution" unit="m" scales="time/year, space/base_geometry">
        <Mean type="float" scales="global">5</Mean>
        <SD type="float" scales="global">1</SD> 
    </InCropBuffer>

## In Field Margin

**Type**: float, xCropProtection.NormalDistribution, or xCropProtection.UniformDistribution

**Unit**: m (meter)

**Scales**:
- Constant: global
- Normal/Uniform distribution: time/year, space/base_geometry|time/day, space/base_geometry

**Notes**:
- A value less than 0 will not increase field size.
</ul>

Constant in field margin:

    <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>

In field margin with a uniform distribution:

    <InFieldMargin type="xCropProtection.UniformDistribution" unit="m" scales="time/year, space/base_geometry">
        <Lower type="float" scales="global">5</Lower>
        <Upper type="float" scales="global">10</Upper> 
    </InFieldMargin>

In field margin with a normal distribution:

    <InFieldMargin type="xCropProtection.NormalDistribution" unit="m" scales="time/year, space/base_geometry">
        <Mean type="float" scales="global">5</Mean>
        <SD type="float" scales="global">1</SD> 
    </InFieldMargin>


## Minimum Applied Area

**Type**: float, xCropProtection.NormalDistribution, or xCropProtection.UniformDistribution

**Unit**: m² (meter²)

**Scales**:
- Constant: global
- Normal/Uniform distribution: time/year, space/base_geometry|time/day, space/base_geometry

**Notes**:
- If a field's area is smaller than this number before or after applying the in crop buffer and in field margin no application will occur.
</ul>

Constant minimum applied area:

    <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>

Minimum applied area with a uniform distribution:

    <MinimumAppliedArea type="xCropProtection.UniformDistribution" unit="m" scales="time/year, space/base_geometry">
        <Lower type="float" scales="global">100</Lower>
        <Upper type="float" scales="global">150</Upper> 
    </MinimumAppliedArea>

Minimum applied area with a normal distribution:

    <MinimumAppliedArea type="xCropProtection.NormalDistribution" unit="m²" scales="time/year, space/base_geometry">
        <Mean type="float" scales="global">100</Mean>
        <SD type="float" scales="global">5</SD> 
    </MinimumAppliedArea>