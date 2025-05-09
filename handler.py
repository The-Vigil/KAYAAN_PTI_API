import runpod
import base64
from openai import OpenAI
import os
import time
import json
from dotenv import load_dotenv
import openai
print("OpenAI version:", openai.__version__)
load_dotenv()
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# %% Component Prompt Registry
PROMPT_REGISTRY = {
    "truck_steering_tires": {
        "system_prompt": """Analyze steering tire image for safety and compliance:
1. Tread depth measurement (minimum 4/32")
2. Sidewall condition (no cuts, bulges, damage)
3. Inflation status (visual assessment)
4. Mounting security (all lug nuts present and tight)
5. Rim condition (no cracks or damage)
If image does not show steering tires, mark component_match as incorrect.
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "tread_depth_32nds": number,
    "pressure_status": "normal|low|high",
    "wear_type": "even|inner|outer|irregular",
    "sidewall_condition": "good|damaged",
    "lug_nut_status": "complete|missing",
    "rim_integrity": "good|damaged",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_rear_tires": {
        "system_prompt": """Analyze rear tire set for safety and compliance:
1. Inter-tire clearance (minimum 1 inch)
2. Matching tread patterns
3. Debris between tires
4. Inflation consistency
5. Tread depth (minimum 2/32")
6. Dual tire matching
If image does not show rear tire set, mark component_match as incorrect.
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "clearance_inches": number,
    "debris_present": boolean,
    "inflation_match": boolean,
    "tread_depth_32nds": number,
    "tire_matching": "matched|mismatched",
    "wear_pattern": "even|uneven",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_mirrors": {
        "system_prompt": """Analyze truck mirrors for safety and compliance:
1. Mount security
2. Surface integrity
3. Proper positioning
4. Coverage angle
5. Hood/fender mirror condition
If image does not show truck mirrors, mark component_match as incorrect.
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "mount_secure": boolean,
    "surface_condition": "clear|damaged",
    "position_correct": boolean,
    "coverage_adequate": boolean,
    "fender_mirror_status": "intact|damaged|missing",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_bumper": {
        "system_prompt": """Analyze truck bumper for safety and compliance:
1. Mount security
2. Height alignment
3. Structural integrity
4. No sagging
If image does not show truck bumper, mark component_match as incorrect
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "mount_secure": boolean,
    "height_correct": boolean,
    "structural_integrity": "good|compromised",
    "sagging_present": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_lights": {
        "system_prompt": """Analyze truck head lighting for safety and compliance:
1. All lights ON in image
2. Proper color (amber/red)
3. Lens condition
4. Even brightness
5. Proper mounting
If image does not show truck head lights, mark component_match as incorrect.
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "lights_functional": boolean,
    "color_correct": boolean,
    "lens_condition": "clear|damaged",
    "brightness_even": boolean,
    "mount_secure": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_mud_flaps": {
        "system_prompt": """Analyze Truck mud flaps for safety and compliance:
1. Proper height from ground
2. Secure mounting
3. No damage/tears
4. Width coverage
5. Anti-spray compliance
If image does not show truck mud flaps, mark component_match as incorrect.
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "height_correct": boolean,
    "mount_secure": boolean,
    "condition": "good|damaged",
    "width_adequate": boolean,
    "spray_compliant": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },
        "trailer_mud_flaps": {
        "system_prompt": """Analyze Trailer mud flaps for safety and compliance:
1. Proper height from ground
2. Secure mounting
3. No damage/tears
4. Width coverage
5. Anti-spray compliance
If image does not show Trailer mud flaps, mark component_match as incorrect.
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "height_correct": boolean,
    "mount_secure": boolean,
    "condition": "good|damaged",
    "width_adequate": boolean,
    "spray_compliant": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "windshield_wipers": {
        "system_prompt": """Analyze windshield and wipers for safety:
1. Windshield integrity
2. Wiper blade condition
3. Wiper arm function
4. Proper coverage
If image does not show windshield and wipers, mark component_match as incorrect
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "windshield_condition": "clear|damaged",
    "blade_condition": "good|worn|damaged",
    "arm_function": "normal|impaired",
    "coverage_complete": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "under_hood_fluid_inspection": {
        "system_prompt": """Analyze under hood fluid levels - MUST see actual fluid line, not just container:
1. Check fluid line against MIN/MAX marks
2. Verify fluid is visible (not just empty container)
3. Check for leaks/stains
4. Verify normal fluid colors
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
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
    "colors_normal": boolean,
    "remark": string
}"""
    },
    "truck_engine_oil": {
        "system_prompt": """Analyze truck engine oil level and condition:
1. Oil level against MIN/MAX marks
2. Oil color check (normal/dark/contaminated)
3. Dipstick condition check
4. Check for leaks around dipstick
5. Oil clarity assessment
If image does not show engine oil dipstick/level indicator, mark component_match as incorrect.
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "oil_level": "full|low|empty",
    "oil_color": "normal|dark|contaminated",
    "dipstick_condition": "good|damaged",
    "leaks_present": boolean,
    "clarity": "clear|cloudy",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_engine_coolant": {
        "system_prompt": """Analyze truck engine coolant level and condition:
1. Coolant level against MIN/MAX marks
2. Coolant color check
3. Reservoir condition
4. Cap security check
5. Check for leaks/overflow
If image does not show coolant reservoir/radiator cap, mark component_match as incorrect.
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "coolant_level": "full|low|empty",
    "coolant_color": "normal|discolored",
    "reservoir_condition": "good|damaged",
    "cap_secure": boolean,
    "leaks_present": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "truck_washer_fluid": {
        "system_prompt": """Analyze truck washer fluid level and condition:
1. Fluid level against MIN/MAX marks
2. Fluid color check
3. Reservoir condition
4. Cap security check
5. Check for leaks
If image does not show washer fluid reservoir, mark component_match as incorrect.
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "fluid_level": "full|low|empty",
    "fluid_color": "normal|discolored",
    "reservoir_condition": "good|damaged",
    "cap_secure": boolean,
    "leaks_present": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "trailer_inspection": {
        "system_prompt": """Analyze trailer condition and compliance:
1. Body panel condition
2. Reflective tape status
3. Door seals/operation
4. Landing gear condition
5. Coupling security

If image does not show trailer body and components, mark component_match as incorrect
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "body_condition": "good|damaged",
    "reflective_tape": "complete|incomplete",
    "door_seals": "good|damaged",
    "landing_gear": "functional|damaged",
    "coupling_secure": boolean,
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "trailer_tires": {
        "system_prompt": """Analyze trailer tires for safety:
1. Tread depth (minimum 2/32")
2. Matching pairs
3. Proper spacing
4. Inflation status

If image does not show trailer tires, mark component_match as incorrect.
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "tread_depth_32nds": number,
    "pairs_matched": boolean,
    "spacing_adequate": boolean,
    "inflation_status": "normal|low|high",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    },

    "trailer_lights": {
        "system_prompt": """Analyze trailer lighting systems:
1. Brake lights function
2. Turn signals
3. Marker lights
4. Reflector condition
If image does not show trailer lights, mark component_match as incorrect
Return JSON: {
    "status": "pass|fail",
    "confidence": 0-1,
    "brake_lights": "functional|failed",
    "turn_signals": "functional|failed",
    "markers": "complete|incomplete",
    "reflectors": "good|damaged",
    "component_match": "correct|incorrect",
    "remark":"Remark"
}"""
    }
}

async def async_handler(job):
    try:
        start_time = time.time()
        print("\n=== New Vehicle Inspection Request Started ===")
        
        # Get input from job
        job_input = job["input"]
        
        # Validate input
        if "image" not in job_input or "component_type" not in job_input:
            raise ValueError("Missing required input: 'image' and 'component_type' required")
            
        component_type = job_input["component_type"]
        if component_type not in PROMPT_REGISTRY:
            raise ValueError(f"Unsupported component type: {component_type}")

        # Get image
        image_base64 = job_input["image"]
        
        # Vision API Analysis
        print("Starting vision analysis...")
        analysis_start = time.time()
        
        messages = [
            {
                "role": "system",
                "content": PROMPT_REGISTRY[component_type]["system_prompt"]
            },
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}",
                        "detail": "high"
                    }},
                    {"type": "text", "text": "Analyze this image and provide the required JSON output."}
                ]
            }
        ]
        try:
        
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            print("API Response:", completion)
        except Exception as e:
            print("Full error details:", str(e)) 
        
        analysis_result = json.loads(completion.choices[0].message.content)
        print(f"Vision analysis took {time.time() - analysis_start:.2f}s")
        
        # Return result
        final_result = {
            "component_type": component_type,
            "analysis_result": analysis_result,
            "processing_time": f"{time.time() - start_time:.2f}s"
        }
        
        print(f"Total request time: {time.time() - start_time:.2f}s")
        return final_result
        
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        return {"error": str(e)}

print("Starting Vehicle Inspector server...")
print("Server ready!")

# async def async_handler(job):
#     try:
#         start_time = time.time()
#         print("\n=== New Vehicle Inspection Request Started ===")
#         print("OpenAI Version:", openai.__version__)  # Debug: Print OpenAI version
        
#         # Debug: Check API Key
#         api_key = os.getenv('OPENAI_API_KEY')
#         print("API Key present:", bool(api_key))
#         if not api_key:
#             raise ValueError("OpenAI API key is missing")
        
#         # Get and validate input
#         job_input = job["input"]
#         print("Received job input keys:", job_input.keys())  # Debug: Print available keys
        
#         # Validate required fields
#         if "image" not in job_input or "component_type" not in job_input:
#             raise ValueError("Missing required input: 'image' and 'component_type' required")
            
#         component_type = job_input["component_type"]
#         print(f"Processing component type: {component_type}")  # Debug: Print component type
        
#         if component_type not in PROMPT_REGISTRY:
#             raise ValueError(f"Unsupported component type: {component_type}")

#         # Get image and validate
#         image_base64 = job_input["image"]
#         print(f"Image data length: {len(image_base64)}")  # Debug: Print image data length
        
#         if not image_base64:
#             raise ValueError("Empty image data received")
        
#         # Vision API Analysis
#         print("Starting vision analysis...")
#         analysis_start = time.time()
        
#         # Construct messages with debug prints
#         system_prompt = PROMPT_REGISTRY[component_type]["system_prompt"]
#         print(f"System prompt length: {len(system_prompt)}")  # Debug: Print prompt length
        
#         messages = [
#             {
#                 "role": "system",
#                 "content": system_prompt
#             },
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{image_base64}",
#                             "detail": "high"
#                         }
#                     },
#                     {
#                         "type": "text",
#                         "text": "Analyze this image and provide the required JSON output."
#                     }
#                 ]
#             }
#         ]
        
#         print("Messages structure constructed")  # Debug: Confirm messages structure
        
#         # API call with enhanced error handling
#         try:
#             print("Attempting API call...")  # Debug: Mark start of API call
#             completion = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=messages,
#                 temperature=0.1,
#                 max_tokens=500,
#                 response_format={"type": "json_object"}
#             )
#             print("API call successful")  # Debug: Mark successful API call
            
#         except openai.APIError as api_err:
#             print(f"OpenAI API Error: {str(api_err)}")
#             print("Error response:", api_err.response if hasattr(api_err, 'response') else "No response details")
#             raise
#         except Exception as e:
#             print(f"Unexpected error during API call: {str(e)}")
#             raise
        
#         # Parse response
#         try:
#             analysis_result = json.loads(completion.choices[0].message.content)
#             print("Successfully parsed JSON response")  # Debug: Confirm JSON parsing
#         except json.JSONDecodeError as json_err:
#             print(f"JSON parsing error: {str(json_err)}")
#             print("Raw response content:", completion.choices[0].message.content)
#             raise
        
#         print(f"Vision analysis took {time.time() - analysis_start:.2f}s")
        
#         # Prepare final result
#         final_result = {
#             "component_type": component_type,
#             "analysis_result": analysis_result,
#             "processing_time": f"{time.time() - start_time:.2f}s"
#         }
        
#         print(f"Total request time: {time.time() - start_time:.2f}s")
#         print("Final result prepared successfully")  # Debug: Confirm final preparation
        
#         return final_result
        
#     except Exception as e:
#         print(f"Error in handler: {str(e)}")
#         print(f"Error type: {type(e).__name__}")  # Debug: Print error type
#         print(f"Error traceback: {traceback.format_exc()}")  # Debug: Print full traceback
#         return {"error": str(e), "error_type": type(e).__name__}



runpod.serverless.start({
    "handler": async_handler
})
