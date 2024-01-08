// Add an event listener for the DOMContentLoaded event. This event is fired when the initial HTML document has been completely loaded and parsed
document.addEventListener('DOMContentLoaded', (event) => {
    // Add a click event listener to the element with the id 'add'
    document.getElementById('add').addEventListener('click', function() {
        // Create a new div element with the class 'input-group'
        var newInputGroup = document.createElement('div');
        newInputGroup.className = 'input-group';

        // Create a new input element for the preset
        var newPresetInput = document.createElement('input');
        newPresetInput.type = 'text';
        newPresetInput.name = 'preset' + (document.getElementsByClassName('input-group').length + 1);
        newPresetInput.placeholder = 'Preset ' + (document.getElementsByClassName('input-group').length + 1);

        // Create a new input element for the sleep time
        var newSleepTimeInput = document.createElement('input');
        newSleepTimeInput.type = 'text';
        newSleepTimeInput.name = 'sleep_time' + (document.getElementsByClassName('input-group').length + 1);
        newSleepTimeInput.placeholder = 'Sleep Time ' + (document.getElementsByClassName('input-group').length + 1);

        // Append the new input elements to the new input group
        newInputGroup.appendChild(newPresetInput);
        newInputGroup.appendChild(newSleepTimeInput);

         // Append the new input group to the element with the id 'inputs'
        document.getElementById('inputs').appendChild(newInputGroup);
    });

    // Add a click event listener to the element with the id 'remove'.
    document.getElementById('remove').addEventListener('click', function() {
        var inputGroups = document.getElementsByClassName('input-group');
        if (inputGroups.length > 0) {
            // If there are any input groups, remove the last one.
            inputGroups[inputGroups.length - 1].remove();

            // Send a POST request to the '/delete_last' endpoint.
            fetch('/delete_last', { method: 'POST' });
        }
    });
    
    // Set an interval to fetch the status from the '/status' endpoint every 2 seconds.
    setInterval(function() {
        fetch('/status')
            .then(response => response.text())
            .then(status => {
                // Update the text content of the element with the id 'status'.
                document.getElementById('status').textContent = 'Volaný preset: ' + status;
            });
    }, 2000);

});