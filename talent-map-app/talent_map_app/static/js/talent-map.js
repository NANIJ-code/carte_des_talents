// This file contains JavaScript code for generating and interacting with the talent map visualization.

document.addEventListener('DOMContentLoaded', function() {
    const talentMapContainer = document.getElementById('talent-map');
    
    if (talentMapContainer) {
        // Initialize the talent map visualization
        initializeTalentMap();
    }

    function initializeTalentMap() {
        // Sample data for talent map
        const userData = [
            { name: 'Alice', skills: ['Python', 'Django'], verified: true },
            { name: 'Bob', skills: ['JavaScript', 'React'], verified: false },
            { name: 'Charlie', skills: ['Java', 'Spring'], verified: true }
        ];

        // Create a visualization for each user
        userData.forEach(user => {
            const userElement = document.createElement('div');
            userElement.classList.add('user-talent');

            const userName = document.createElement('h3');
            userName.textContent = user.name;

            const userSkills = document.createElement('p');
            userSkills.textContent = 'Skills: ' + user.skills.join(', ');

            if (user.verified) {
                const verifiedBadge = document.createElement('span');
                verifiedBadge.textContent = 'Talent Verified';
                verifiedBadge.classList.add('badge', 'badge-success');
                userElement.appendChild(verifiedBadge);
            }

            userElement.appendChild(userName);
            userElement.appendChild(userSkills);
            talentMapContainer.appendChild(userElement);
        });
    }
});