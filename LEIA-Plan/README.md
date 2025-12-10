# 📝 LEIA-Plan
LEIA-Plan is a laser-etching industrial dataset of atomic events and multi-step workflows, constructed from real operational scenarios involving five-axis CNC machines, dynamic-focusing galvanometers, and pulsed fiber lasers.

## Events
A large number of specific atomic operation commands from laser etching industrial processing scenarios were analyzed and summarized in [events](./events/).

[event-template](events/event-template.json) contains 24 types of event templates, including their categories and parameters. Its wording differs slightly from the *Global Information* in prompts used in TPEE. The table below shows the correspondence between them.

| event-template | Global Information |
| :---: | :---: |
| Machine-File | Machine Formula Selection |
| Machine-Connect | Machine Connection/Disconnection |
| Machine-AxisConfig | Machine Axis Configuration |
| Machine-Parameters | Machine Structural Parameters Setting |
| Machine-AxisEnable | Machine Enable Switch |
| Machine-Move | Machine Movement |
| Machine-Home | Machine Axis Homing |
| Machine-Stop | Machine Stop |
| Board-File | Scanner Correction File Selection |
| Board-Connect | Scanner Connection/Disconnection |
| Board-Parameters | Scanner Parameters Setting |
| Board-Offset| Scanner Offset Setting |
| Camera-File | Camera Calibration File Selection |
| Camera-Select | Camera Selection |
| Laser-Connect | Laser Connection/Disconnection |
| Laser-Operate | Laser Operation |
| Laser-Parameters | Laser Parameter Setting |
| Tool-Parameters | Tool Structural Parameters Setting |
| Tool-Switch | Tool Switching |
| Tool-RetractEnable | Tool Retraction Enable Switch |
| Tool-RetractDistance | Tool Retraction Distance Setting |
| Tool-Move | Tool Movement |
| Process-Parameters | Processing Parameters Setting |
| Process-Operate | Processing Operation |

[event-id](events/event-id.id) and [role-id](events/role-id.id) provide ID-based encoding for events and parameters, making it easier to train the Atomic-Event Classifier and the Event-Extraction Model in TPEE.

[atomic-event-data](events/atomic-event-data.json) contains 672 common atomic operations in industrial processing, along with their event classification results.

<!-- 24 types of atomic events encompassing 25 parameters in total. Among these parameters, 9 parameters can be directly extracted from atomic events without further classification and are referred to as continuous parameters. The remaining 16 parameters require further classification after extraction and are referred to as discrete parameters. These discrete parameters can be further divided into 66 categories. -->

⏳ *Other details will be updated soon.*