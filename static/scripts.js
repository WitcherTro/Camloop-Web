document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('add').addEventListener('click', function() {
        // Create a new input group
        var newInputGroup = document.createElement('div');
        newInputGroup.className = 'input-group';
        // Create a new preset input
        var newPresetInput = document.createElement('input');
        newPresetInput.type = 'text';
        newPresetInput.name = 'preset' + (document.getElementsByClassName('input-group').length + 1);
        newPresetInput.placeholder = 'Preset ' + (document.getElementsByClassName('input-group').length + 1);
        // Create a new sleep time input
        var newSleepTimeInput = document.createElement('input');
        newSleepTimeInput.type = 'text';
        newSleepTimeInput.name = 'sleep_time' + (document.getElementsByClassName('input-group').length + 1);
        newSleepTimeInput.placeholder = 'Sleep Time ' + (document.getElementsByClassName('input-group').length + 1);
        // Add the new input fields to the form
        newInputGroup.appendChild(newPresetInput);
        newInputGroup.appendChild(newSleepTimeInput);
        document.getElementById('inputs').appendChild(newInputGroup);
    });

    document.getElementById('remove').addEventListener('click', function() {
        var inputGroups = document.getElementsByClassName('input-group');
        if (inputGroups.length > 0) {
            // Remove the last input group
            inputGroups[inputGroups.length - 1].remove();

            // Send a POST request to the server to delete the last preset
            fetch('/delete_last', { method: 'POST' });
        }
    });
    
    setInterval(function() {
        fetch('/status')
            .then(response => response.text())
            .then(status => {
                document.getElementById('status').textContent = 'Volany preset: ' + status;
            });
    }, 2000);

});
window.onload = function() {
    var status = document.getElementById('status').textContent;
    if (status.includes('bezi')) {
        var inputs = document.getElementsByTagName('input');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].disabled = true;
        }
    }
}