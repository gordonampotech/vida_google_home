import os
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.util.yaml import load_yaml, dump_yaml

from .const import (
    DOMAIN, 
    GOOGLE_ASSISTANT, 
    PROJECT_ID, 
    SERVICE_ACCOUNT, 
    REPORT_STATE, 
    JSON_FILE
)

# Define the schema for user input, requiring a project_id
DATA_SCHEMA = vol.Schema({
    vol.Required(PROJECT_ID): str,
    vol.Required(JSON_FILE): cv.isfile,
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Vida Google Home."""

    # Asynchronous function to save configuration to configuration.yaml
    async def save_to_configuration(self, hass, data):
        config_path = hass.config.path("configuration.yaml")
        
        # Load current configuration
        current_config = await hass.async_add_executor_job(load_yaml, config_path)
        
        # Update configuration with new project_id under google_assistant key
        if GOOGLE_ASSISTANT not in current_config:
            current_config[GOOGLE_ASSISTANT] = {}
        
        # add project_id to the configuration.yaml file
        current_config[GOOGLE_ASSISTANT].update(data)
        current_config[GOOGLE_ASSISTANT].update({ SERVICE_ACCOUNT: "!include SERVICE_ACCOUNT.JSON" })
        current_config[GOOGLE_ASSISTANT].update({ REPORT_STATE: True })
        
        # Write the updated configuration back to the file
        await hass.async_add_executor_job(
            dump_yaml, current_config, config_path
        )

    def save_json_file(self, json_file):
        config_path = self.hass.config.path()
        target_path = os.path.join(config_path, os.path.basename(json_file.filename))
        with open(target_path, 'wb') as f:
            f.write(json_file.file.read())
        return target_path
    
    # Initial user step in the configuration flow
    @callback
    async def async_step_user(self, user_input=None):
        errors = {}
        # If user has submitted the form
        if user_input is not None:
            project_id = user_input.get(PROJECT_ID)
            json_file = user_input.get(JSON_FILE)

            if json_file:
                try:
                    file_path = self.save_json_file(json_file)
                    # Save the configuration
                    await self.save_to_configuration({"project_id": project_id, "json_file_path": file_path})
                    return self.async_create_entry(title="Vida Google Home", data=user_input)
                except Exception as e:
                    errors["base"] = str(e)

        # Show the form to the user to get input
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)
