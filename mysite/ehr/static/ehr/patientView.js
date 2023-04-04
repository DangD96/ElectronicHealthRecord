document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#meds').addEventListener('click', loadMedsView);
    const medsView = document.querySelector('#medsView');
    const addMedsView = document.querySelector('#addMedsView');
    const messageView = document.querySelector('#messageView');

    const messageTab = document.querySelector('#message');
    if (messageTab !== null) {
        messageTab.addEventListener('click', loadMessageView); // Only add event listener if patient has email on file
    }

    loadMedsView(); // Default to Meds view
})

function loadMedsView() {
    const existingMeds = document.querySelector('#existingMeds');
    const patient_id = document.querySelector('#patientID').innerHTML;
    medsView.style.display = 'block';
    addMedsView.style.display = 'block';
    messageView.style.display = 'none';

    // Use then() to wait for promise to resolve
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/then
    // fetch() works too, but just trying something different
    getPatientMeds(patient_id).then((meds) => {
        if (meds.length > 0) {
            const medGroup = document.querySelector('#existingMeds');
            for (let med of meds) {
                const groupDiv = document.createElement('div');
                groupDiv.className = 'list-group';

                const groupItemDiv = document.createElement('div');
                groupItemDiv.classList.add('list-group-item', 'list-group-item-action'); // https://developer.mozilla.org/en-US/docs/Web/API/DOMTokenList/add
                const contentDiv = document.createElement('div');
                contentDiv.classList.add('d-flex', 'w-100', 'justify-content-between')
                const medName = document.createElement('h5');
                medName.id = 'medName';
                medName.className = 'mb-1';
                medName.innerHTML = `${med.name}`;
                contentDiv.append(medName);
                groupItemDiv.append(contentDiv);

                const medDose = document.createElement('p');
                medDose.id = 'medDose';
                medDose.className = 'mb-1';
                medDose.innerHTML = `Dosage: ${med.dose} ${med.doseUnits}`
                groupItemDiv.append(medDose);

                groupDiv.append(groupItemDiv);
                medGroup.append(groupDiv);
            }
        } else {
            const noMeds = document.createElement('h4');
            noMeds.innerHTML = 'This patient currently has no meds on file.'
            existingMeds.innerHTML = '';
            existingMeds.append(noMeds);
        }
    })
}

function loadMessageView() {
    medsView.style.display = 'none';
    addMedsView.style.display = 'none';
    messageView.style.display = 'block';
}

// async keyword makes function return a promise
// await keyword waits for promise to resolve (fetch itself returns a promise too)
// https://www.w3schools.com/js/js_async.asp
async function getPatientMeds(id) {
    const response = await fetch(`/get_meds/${id}`) // fetch() returns promise that resolves to the 'thing' that's returned
    const meds = await response.json(); // json() is also asynchronous and returns a promise
    return meds["patientMeds"]; // returns this as a promise
}

