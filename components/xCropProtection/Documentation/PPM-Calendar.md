Work in progress

# What is a PPM Calendar?

A PPM Calendar is an implementation of an application calendar - a set of information about what a grower may apply, when products may be applied, and how they may be applied. This includes any restrictions on applications.

# Elements of a PPM Calendar

The following is a description of each element in a PPMCalendar. For more technical documentation, see [ppm-calendar-code.md](ppm-calendar-code.md)

## Temporal Validity

Temporal validity of the PPM Calendar. Set 'always' if the PPM Calendar should be applied over the whole simulation. This defines the set of dates that the PPM Calendar is valid over.

## Target Crops

The target crops for this PPM Calendar. This can be one or more crop type, with all crop types specified here receiving the same application parameters as defined in the rest of the PPM Calendar. Crop types are specified as an integer value.

## Indications

A list of one or more indications. During the execution of xCP, an application sequence from each indication will be selected to be applied to a specific field.

## Indication

An event that requires a product to be applied (e.g., signs of insects, weeds appearing, or plant growth stages). An indication contains a choice list of application sequences, whose probabilities must sum to 1.0.

## Application Sequence

A sequence of one or more separate applications. Each application sequence includes a probability of occurring, which must total 1.0 along with other application sequences in the indication. If an application sequence has more than 1 application, all applications in that sequence will be performed on the same field.

## Application

A description of a single application. An application contains a tank, application window, technology, in crop buffer, in field margin, and minimum applied area. These elements are described in the following sections.

### Tank

A representation of the contents of the tank as the grower is applying product(s) to fields. Nothing is defined in the tank element, however, it serves as a parent for the elements which define products and application rates.

### Products

A list of names of one or more products combined in a tank, with multiple products separated by a | character. Products may have spaces in their names.

### Application Rates

A list of application rates for prducts in the tank. The number of application rates should be equal to the number of products in the tank. Each application rate is decribed using one of the following random variables:
- Normal distribution
- Uniform distribution
- Discrete uniform distribution
- Choice distribution

### Application Window

The range of possible dates that an application can occur.

### Technology

Describes a technology and its properties. Technologies include a name and a drift reduction factor, which is the factor by which spray-drift is reduced by technological measures. The value of this element should be the name of a technology in a [Technologies.xml](technologies.md) file

### In Crop Buffer

An in-crop buffer used during applications. Crops within this number of units from the edge of the field are not treated.

### In Field Margin

A margin without crops within fields.

### Minimum Applied Area

The minimum area a field must have to receive an application. Any fields with an area smaller than this number will not receive an application.