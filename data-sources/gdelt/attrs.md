### **Event Table Attributes**

Source: http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf

*   **GlobalEventID**: This is a globally unique identifier assigned to each event record in the master dataset. It identifies the record uniquely but should not be used to sort events by date.
*   **Day**: This field records the date the event took place in YYYYMMDD format. It provides the primary daily temporal resolution for historical event analysis.
*   **MonthYear**: This provides an alternative formatting of the event date in YYYYMM format. It is designed for analytical software that requires specific date formats.
*   **Year**: This is an alternative formatting of the event date in YYYY format. It allows for easy aggregation of events by year.
*   **FractionDate**: This expresses the event date as YYYY.FFFF, where the fractional part represents the percentage of the year completed. It offers a single-number mechanism to estimate the rough temporal distance between dates.
*   **Actor1Code**: The complete raw CAMEO code for Actor1, concatenating geographic, ethnic, religious, and role classes. It describes the characteristics of the first actor involved in the event.
*   **Actor1Name**: The actual human-readable name of Actor1, such as a leader's name, organization, or country. It is used to identify the primary participant in the interaction.
*   **Actor1CountryCode**: The 3-character CAMEO code representing the country affiliation of Actor1. This field reflects a combination of information from the actor dictionary and the source text.
*   **Actor1KnownGroupCode**: Contains the CAMEO code if Actor1 is identified as a known IGO, NGO, or rebel organization. It helps track specific established non-state actors.
*   **Actor1EthnicCode**: The CAMEO code for the ethnic affiliation of Actor1, if specified in the source document. This tracking is considered experimental and derived from specific dictionaries.
*   **Actor1Religion1Code**: The primary CAMEO code for the religious affiliation of Actor1. It identifies the religious group associated with the actor in the text.
*   **Actor1Religion2Code**: Contains a secondary religious code if multiple affiliations are specified for Actor1. Some entries, like "Catholic," automatically trigger two codes (Christianity and Catholicism).
*   **Actor1Type1Code**: The 3-character CAMEO code identifying the functional role or "type" of Actor1, such as Military or Government. It describes the actor's position or role in their environment.
*   **Actor1Type2Code**: Returns the second role code if multiple types are specified for Actor1. It provides additional descriptive detail for the actor's role.
*   **Actor1Type3Code**: Returns the third role code if Actor1 has three specified types or roles. This allows for complex descriptions of multi-faceted actors.
*   **Actor2Code**: The complete raw CAMEO code for the second actor (Actor2) involved in the event. It follows the same definition and structure as the Actor1Code.
*   **Actor2Name**: The formal name of the second participant in the event interaction. It identifies who Actor1 acted upon.
*   **Actor2CountryCode**: The 3-character CAMEO code for the country affiliation of Actor2. Like the Actor1 version, it identifies the actor's national association.
*   **Actor2KnownGroupCode**: The specific organization or group code assigned to Actor2 if they are a known entity. It captures affiliations for NGOs, IGOs, or rebel groups.
*   **Actor2EthnicCode**: The identified ethnic affiliation code for Actor2 found in the document. It tracks the ethnic background of the second participant.
*   **Actor2Religion1Code**: The primary religious affiliation code for Actor2. It records the religion identified for the second actor in the text.
*   **Actor2Religion2Code**: The secondary religious code if multiple affiliations are listed for Actor2. It functions identically to the Actor1Religion2Code.
*   **Actor2Type1Code**: The primary 3-character code describing the role or functional type of Actor2. It identifies whether the second actor is a civilian, police, etc.
*   **Actor2Type2Code**: The second role code assigned to Actor2 if multiple roles are identified. It provides more granular detail on the second actor's position.
*   **Actor2Type3Code**: The third role code for Actor2 when three functional roles are specified. This captures the final layer of role identification for the second participant.
*   **IsRootEvent**: A flag indicating if the event appeared in the lead paragraph of the first document that reported it. It serves as a legacy proxy for determining the rough "importance" of an event.
*   **EventCode**: The raw CAMEO action code describing the interaction Actor1 performed on Actor2. This is the core classification of the action within the event.
*   **EventBaseCode**: The level-two leaf root node of the CAMEO taxonomy for the action. It allows for aggregating specific event codes into broader categories.
*   **EventRootCode**: The root-level category (level one) that the event code falls under. This is used for high-level analysis and aggregation of event actions.
*   **QuadClass**: A numeric code (1–4) classifying the action into Verbal Cooperation, Material Cooperation, Verbal Conflict, or Material Conflict. It provides the highest level of aggregation for analyzing event types.
*   **GoldsteinScale**: A numeric score from -10 to +10 representing the theoretical impact the action has on a country's stability. It estimates the potential impact based on the event type rather than the specific event's scale.
*   **NumMentions**: The total count of mentions of this event across all documents in the 15-minute window it was first seen. It is used as a legacy measure to assess the initial significance of an event.
*   **NumSources**: The total number of unique information sources that mentioned the event in its first 15-minute observation. This metric gauges the initial breadth of the media's attention.
*   **NumArticles**: The number of source documents that mentioned the event during the initial 15-minute update. It helps evaluate the density of coverage for a new event record.
*   **AvgTone**: The average "tone" (from -100 to +100) of all documents mentioning the event in its first 15 minutes. It serves as a proxy for the emotional context or impact of the event.
*   **Actor1Geo_Type**: Specifies the geographic resolution of the match for Actor1, such as Country, City, or State. It helps filter events based on how specifically the location was identified.
*   **Actor1Geo_Fullname**: The human-readable name of the location identified for Actor1. This name reflects the precise spelling used in the source text.
*   **Actor1Geo_CountryCode**: The 2-character FIPS10-4 country code for the location associated with Actor1. It provides a standardized identifier for the actor's country location.
*   **Actor1Geo_ADM1Code**: The combined FIPS country and administrative division (ADM1) code for Actor1's location. It identifies regional divisions like US states.
*   **Actor1Geo_ADM2Code**: The numeric GAUL or FIPS/county code for second-order administrative divisions for Actor1. It provides granular administrative georeferencing when available.
*   **Actor1Geo_Lat**: The centroid latitude coordinate for the landmark identified for Actor1. It is used for mapping the actor's estimated position.
*   **Actor1Geo_Long**: The centroid longitude coordinate for the landmark identified for Actor1. This coordinate facilitates spatial analysis of the actor.
*   **Actor1Geo_FeatureID**: The GNS or GNIS FeatureID that uniquely identifies the specific geographic location for Actor1. It resolves multiple spellings or transliterations to a single unique identifier.
*   **Actor2Geo_Type**: The geographic resolution level (Country, City, etc.) for Actor2's location. It functions exactly like the Actor1 version for the second participant.
*   **Actor2Geo_Fullname**: The human-readable name of the location associated with Actor2 in the text. It records how the location was named in the source document.
*   **Actor2Geo_CountryCode**: The 2-character FIPS country code for Actor2's location. This identifies the country where the second actor was positioned.
*   **Actor2Geo_ADM1Code**: The administrative division 1 code for the location of Actor2. It provides regional georeferencing for the second actor.
*   **Actor2Geo_ADM2Code**: The second-order administrative division code for Actor2's location. It offers granular local georeferencing for the second actor.
*   **Actor2Geo_Lat**: The centroid latitude for the geographic location of Actor2. It provides the map coordinate for the second participant.
*   **Actor2Geo_Long**: The centroid longitude for the geographic location of Actor2. This allows for the spatial placement of Actor2 on a map.
*   **Actor2Geo_FeatureID**: The unique GNS or GNIS identifier for the location of Actor2. It is used to uniquely identify the place regardless of how it was spelled.
*   **ActionGeo_Type**: The geographic resolution level for the location where the event action took place. It identifies the specificity of the event's primary location.
*   **ActionGeo_Fullname**: The human-readable name of the location where the action occurred. This is considered the best location for placing events on a map.
*   **ActionGeo_CountryCode**: The 2-character FIPS country code for the location of the action. It identifies the country where the event actually happened.
*   **ActionGeo_ADM1Code**: The administrative division 1 code for the action's location. It provides regional context for where the event occurred.
*   **ActionGeo_ADM2Code**: The second-order administrative division code for the action's location. It offers the most granular administrative data for the event site.
*   **ActionGeo_Lat**: The centroid latitude for the location of the action. This is the primary coordinate used for mapping the event itself.
*   **ActionGeo_Long**: The centroid longitude for the location of the action. It provides the spatial coordinate for the event's occurrence.
*   **ActionGeo_FeatureID**: The unique GNS or GNIS identifier for the action's location. It resolves the event's location to a unique global feature ID.
*   **DATEADDED**: The 15-minute resolution timestamp (YYYYMMDDHHMMSS) when the event was added to the database. This is the field recommended for querying real-time data at its highest resolution.
*   **SOURCEURL**: The URL or citation of the first news report that mentioned this event. It allows users to access the original source material for the event record.

---

### **Mentions Table Attributes**

*   **GlobalEventID**: The unique ID of the event being mentioned, used to link the mention back to the Event Table. It allows for tracking the "trajectory" of a single event through many reports.
*   **EventTimeDate**: The timestamp (YYYYMMDDHHMMSS) of when the event was first recorded by GDELT. It can be compared to the mention time to identify breaking news or anniversary mentions.
*   **MentionTimeDate**: The 15-minute timestamp (YYYYMMDDHHMMSS) of the current update for the mention. It records exactly when the specific news report was processed.
*   **MentionType**: A numeric identifier for the source collection, such as Web, Citation, or JSTOR. It tells the system how to interpret the MentionIdentifier to find the document.
*   **MentionSourceName**: A human-friendly identifier for the document's source, like a top-level domain or "BBC Monitoring". It is used for network analysis of information flows by source.
*   **MentionIdentifier**: The unique external identifier for the source document, such as a URL or DOI. It provides the path to access the specific document containing the mention.
*   **SentenceID**: The sentence number within the article where the event was mentioned. It is used as a measure of the event's prominence within the news report.
*   **Actor1CharOffset**: The character position within the English text where Actor1 was identified. It facilitates precise integration with other text analysis tools like the GKG.
*   **Actor2CharOffset**: The character position within the English text where Actor2 was found. This allows for the exact location of the second actor within the document.
*   **ActionCharOffset**: The character position in the text where the core description of the action was found. It identifies exactly where the interaction was described in the article.
*   **InRawText**: A flag (1 or 0) indicating if the event was found in unaltered raw text or via advanced synthesis. Mentions found in raw text typically represent clearer, more detail-rich references.
*   **Confidence**: A percentage (10–100) reflecting GDELT’s confidence in the extraction of the event from that article. It helps users filter for the most reliable or unambiguous event reports.
*   **MentionDocLen**: The total length of the source document in English characters. This helps distinguish between brief mentions and long, detailed articles.
*   **MentionDocTone**: The tone score specifically for the individual article containing the mention. It provides the specific emotional context for that report.
*   **MentionDocTranslationInfo**: Delimited provenance information for machine-translated documents, including the source language and translation engine. It identifies documents that may have lower accuracy due to machine translation.
*   **Extras**: A field currently reserved for future specialized measurements and is presently blank. It ensures the database can accommodate new data types in the future.