Work in progress

# Building xml inputs

Once you have set up your xCP repository, the next step is to generate input files. Creating a complete input to xCP requires 3 Extensible Markup Language (XML) files located in xCropProtection/scenario/{scenario-name}/xCropProtection.

- [PPMCalendar.xml](PPM-Calendar.md)
- [Technologies.xml](technologies.md)
- [xCropProtection.xml](x-crop-protection.md)

For a more technical description of elements, see [ppm-calendar-code.md](ppm-calendar-code.md)

## PPMCalendar.xml

The general structure of a PPMCalendar.xml is

    <PPMCalendar>
        <TemporalValidity/>
        <TargetCrops/>
        <Indications>
            <Indication>
                <ApplicationSequence>
                    <Application>
                        <Tank>
                            <Products/>
                            <ApplicationRates>
                                <ApplicationRate/>
                            </ApplicationRates>
                        </Tank>
                        <ApplicationWindow/>
                        <Technology/>
                        <InCropBuffer/>
                        <InFieldMargin/>
                        <MinimumAppliedArea/>
                    </Application>
                </ApplicationSequence>
            </Indication>
        </Indications>
    </PPMCalendar>

Example of a simple PPMCalendar.xml:

    <PPMCalendar xmlns="urn:xCropProtectionLandscapeScenarioParametrization">
        <TemporalValidity scales="time/simulation">
            always
        </TemporalValidity>
        <TargetCrops type="list[int]" scales="global">
            1
        </TargetCrops>
        <Indications>
            <Indication type="xCropProtection.ChoiceDistribution" scales="time/year, space/base_geometry">
                <ApplicationSequence probability="1">
                    <Application>
                        <Tank>
                            <Products type="list[str]" scales="other/products">
                                Product 1
                            </Products>
                            <ApplicationRates scales="other/products">
                                <ApplicationRate type="xCropProtection.UniformDistribution" unit="g/ha" scales="time/year, space/base_geometry">
                                    <Lower type="float" scales="global">100</Lower>
                                    <Upper type="float" scales="global">150</Upper> 
                                </ApplicationRate>
                            </ApplicationRates>
                        </Tank>
                        <ApplicationWindow type="xCropProtection.MonthDaySpan">04-15 to 04-31</ApplicationWindow>
                        <Technology scales="global">Technology</Technology>
                        <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>
                        <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>
                        <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>
                    </Application>
                </ApplicationSequence>
            </Indication>
        </Indications>
    </PPMCalendar>


This PPM Calendar will result in fields of crop type 1 having a single application of Product 1 between the days of April 15th and April 31st. The application rate will be chosen randomly using a uniform distribution with the minimum value being 100 and the maximum value being 150.
