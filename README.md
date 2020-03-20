# smartBin
IoT Hack for DeltaHacks VI

## Inspiration 
Waste Management: Despite having bins with specific labels, people often put waste into the wrong bins which can lead to unnecessary plastic/recyclables in landfills.

## The Project
We designed a smart garbage bin than uses a Raspberry Pi, the Google vision API and our custom classifier to categorize waste and automatically sorts and puts them into right sections (Garbage, Organic, Recycle). The data collected is stored in Firebase, and showed with respective category and item label(type of waste) on a web app/console. The web app is capable of providing advanced statistics such as % recycling/compost/garbage, your carbon emissions as well as statistics on which specific items you throw out the most (water bottles, bag of chips, etc.). The classifier is capable of being modified to suit the garbage laws of different places (eg. separate recycling bins for paper and plastic).

