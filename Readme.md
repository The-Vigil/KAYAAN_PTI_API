# KAYAAN Vehicle Inspection Vision API 🚛

## Proprietary Software Notice
© 2025 KAYAAN Technologies. All Rights Reserved.

This software is proprietary and confidential. Unauthorized copying, transfer, or reproduction of the contents of this repository, via any medium, is strictly prohibited.

The receipt or possession of the source code and/or any parts thereof does not convey or imply any right to use them for any purpose other than the purpose for which they were provided to you.

The software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

For licensing inquiries, please contact: [Contact Information]

## Overview
AI-powered visual inspection system for commercial vehicles. The API uses GPT-4 Vision to analyze vehicle components and provide detailed safety and compliance assessments.

## Technical Requirements
```bash
- Python 3.8+
- OpenAI API key
- RunPod environment
- Base64 image processing capabilities
```

## API Usage

### Basic Request Format
```python
{
    "image": "base64_encoded_image",
    "component_type": "component_identifier"
}
```

### Basic Response Format
```python
{
    "component_type": "requested_component_type",
    "analysis_result": {
        "status": "pass|fail",
        "confidence": 0-1,
        "component_match": "correct|incorrect",
        "remark": "String",
        // Component-specific fields
    }
}
```

## Available Component Types

### 1. Truck Tire Systems
#### Steering Tires (`truck_steering_tires`)
```json
{
    "tread_depth_32nds": number,
    "pressure_status": "normal|low|high",
    "wear_type": "even|inner|outer|irregular",
    "sidewall_condition": "good|damaged",
    "lug_nut_status": "complete|missing",
    "rim_integrity": "good|damaged"
}
```

#### Rear Tires (`truck_rear_tires`)
```json
{
    "clearance_inches": number,
    "debris_present": boolean,
    "inflation_match": boolean,
    "tread_depth_32nds": number,
    "tire_matching": "matched|mismatched",
    "wear_pattern": "even|uneven"
}
```

### 2. External Components
#### Mirrors (`truck_mirrors`)
```json
{
    "mount_secure": boolean,
    "surface_condition": "clear|damaged",
    "position_correct": boolean,
    "coverage_adequate": boolean,
    "fender_mirror_status": "intact|damaged|missing"
}
```

#### Bumper (`truck_bumper`)
```json
{
    "mount_secure": boolean,
    "height_correct": boolean,
    "structural_integrity": "good|compromised",
    "sagging_present": boolean
}
```

#### Lights (`truck_lights`)
```json
{
    "lights_functional": boolean,
    "color_correct": boolean,
    "lens_condition": "clear|damaged",
    "brightness_even": boolean,
    "mount_secure": boolean
}
```

### 3. Protection Systems
#### Truck Mud Flaps (`Truck_mud_flaps`)
```json
{
    "height_correct": boolean,
    "mount_secure": boolean,
    "condition": "good|damaged",
    "width_adequate": boolean,
    "spray_compliant": boolean
}
```

#### Trailer Mud Flaps (`Trailer_mud_flaps`)
```json
{
    "height_correct": boolean,
    "mount_secure": boolean,
    "condition": "good|damaged",
    "width_adequate": boolean,
    "spray_compliant": boolean
}
```

### 4. Visibility Systems
#### Windshield and Wipers (`windshield_wipers`)
```json
{
    "windshield_condition": "clear|damaged",
    "blade_condition": "good|worn|damaged",
    "arm_function": "normal|impaired",
    "coverage_complete": boolean
}
```

### 5. Fluid Systems
#### Under Hood Fluid Inspection (`under_hood_fluid_inspection`)
```json
{
    "washer_fluid": {
        "level": "full|low|empty",
        "fluid_visible": boolean
    },
    "coolant": {
        "level": "full|low|empty",
        "fluid_visible": boolean
    },
    "oil": {
        "level": "full|low|empty",
        "fluid_visible": boolean
    },
    "leaks_detected": boolean,
    "colors_normal": boolean
}
```

#### Engine Oil (`truck_engine_oil`)
```json
{
    "oil_level": "full|low|empty",
    "oil_color": "normal|dark|contaminated",
    "dipstick_condition": "good|damaged",
    "leaks_present": boolean,
    "clarity": "clear|cloudy"
}
```

#### Engine Coolant (`truck_engine_coolant`)
```json
{
    "coolant_level": "full|low|empty",
    "coolant_color": "normal|discolored",
    "reservoir_condition": "good|damaged",
    "cap_secure": boolean,
    "leaks_present": boolean
}
```

#### Washer Fluid (`truck_washer_fluid`)
```json
{
    "fluid_level": "full|low|empty",
    "fluid_color": "normal|discolored",
    "reservoir_condition": "good|damaged",
    "cap_secure": boolean,
    "leaks_present": boolean
}
```

### 6. Trailer Components
#### General Inspection (`trailer_inspection`)
```json
{
    "body_condition": "good|damaged",
    "reflective_tape": "complete|incomplete",
    "door_seals": "good|damaged",
    "landing_gear": "functional|damaged",
    "coupling_secure": boolean
}
```

#### Tires (`trailer_tires`)
```json
{
    "tread_depth_32nds": number,
    "pairs_matched": boolean,
    "spacing_adequate": boolean,
    "inflation_status": "normal|low|high"
}
```

#### Lights (`trailer_lights`)
```json
{
    "brake_lights": "functional|failed",
    "turn_signals": "functional|failed",
    "markers": "complete|incomplete",
    "reflectors": "good|damaged"
}
```

## Error Handling
```json
{
    "error": "Error description string"
}
```

Common error types:
- Invalid component type
- Malformed base64 image data
- Component mismatch
- Analysis timeout/failure
- Network connectivity issues
- Invalid image format

## Best Practices

### Image Requirements
- Clear, well-lit images
- Proper angle and distance
- Minimal obstruction
- Focused on the specific component
- Recommended resolution: [Specify]
- Maximum file size: [Specify]

### Implementation Guidelines
1. Always validate component_match field
2. Handle confidence scores appropriately
3. Implement retry logic for failures
4. Log all responses for debugging
5. Monitor response times
6. Handle timeouts gracefully

## System Constraints
- Model: gpt-4-vision-preview
- Max tokens: 500
- Temperature: 0.0
- Response format: JSON
- Image format: Base64 encoded JPEG
- Rate limits: [Specify]

## Access and Security
This repository and API are private and access is restricted to authorized personnel only. Distribution or sharing of any part of this codebase without explicit permission from KAYAAN Technologies is prohibited.

### Security Guidelines
1. Secure storage of API keys
2. Implement rate limiting
3. Monitor usage patterns
4. Regular security audits
5. Access logging

## Support
For technical support and inquiries:
- Email: [Support Email]
- Hours: [Support Hours]
- Emergency Contact: [Emergency Contact]

## Version History
- Current Version: 1.0
- Last Updated: February 22, 2025
- Change Log: Available upon request

---
KAYAAN Technologies - Confidential and Proprietary