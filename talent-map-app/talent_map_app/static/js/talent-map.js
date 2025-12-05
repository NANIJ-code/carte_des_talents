// This file contains JavaScript code for generating and interacting with the talent map visualization.

document.addEventListener('DOMContentLoaded', function () {

    // --- Talent map container (stub) ---
    const talentMapContainer = document.getElementById('talent-map');
    if (talentMapContainer) {
        initializeTalentMap();
    }
    function initializeTalentMap() {
        // placeholder: logique de visualisation
        // console.log('initializeTalentMap');
    }

    // --- Search form validation (safe guard) ---
    const form = document.getElementById('search-form');
    if (form) {
        const qInput = form.querySelector('[name="q"]');
        form.addEventListener('submit', function (e) {
            if (!qInput) return;
            if (qInput.value.trim() === '') {
                e.preventDefault();
                qInput.classList.add('is-invalid');
                let fb = qInput.parentNode.querySelector('.invalid-feedback');
                if (!fb) {
                    fb = document.createElement('div');
                    fb.className = 'invalid-feedback';
                    fb.textContent = "Veuillez saisir un terme de recherche ou une compétence.";
                    qInput.parentNode.appendChild(fb);
                }
                qInput.focus();
            }
        });
        if (qInput) {
            qInput.addEventListener('input', function () {
                qInput.classList.remove('is-invalid');
                const fb = qInput.parentNode.querySelector('.invalid-feedback');
                if (fb) fb.remove();
            });
        }
    }

    // --- Profile card animations: entrance, float and tilt ---
    const card = document.querySelector('.profile-card');
    if (card) {
        setTimeout(() => {
            card.classList.add('animate-in');
            setTimeout(() => card.classList.add('float'), 800);
        }, 80);

        const skills = card.querySelectorAll('.skill-badge');
        skills.forEach((el, i) => setTimeout(() => el.classList.add('animate'), 140 * i));

        const accentBtn = card.querySelector('.btn-accent');
        if (accentBtn) accentBtn.classList.add('pulse');

        let rect = null;
        function onMove(e) {
            if (!rect) rect = card.getBoundingClientRect();
            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            const clientY = e.clientY || (e.touches && e.touches[0].clientY);
            if (clientX == null || clientY == null) return;
            const cx = rect.left + rect.width / 2;
            const cy = rect.top + rect.height / 2;
            const dx = (clientX - cx) / (rect.width / 2);
            const dy = (clientY - cy) / (rect.height / 2);
            const rotX = (dy * 6);
            const rotY = -(dx * 8);
            card.style.transform = `perspective(900px) rotateX(${rotX}deg) rotateY(${rotY}deg)`;
            card.style.boxShadow = `${-rotY}px ${Math.abs(rotX) + 8}px 30px rgba(16,24,40,0.08)`;
        }
        function resetTilt() {
            card.style.transform = '';
            card.style.boxShadow = '';
            rect = null;
        }
        card.addEventListener('mousemove', onMove);
        card.addEventListener('touchmove', onMove, { passive: true });
        card.addEventListener('mouseleave', resetTilt);
        card.addEventListener('touchend', resetTilt);
    }

    // --- Dynamic skills inputs (create/edit/signup) ---
    // Remplacement : supporte plusieurs conteneurs, délégation d'événements et gestion robuste des boutons
    (function () {
        // Crée un élément "skill-item"
        function createSkillItem(value = '') {
            const wrapper = document.createElement('div');
            wrapper.className = 'input-group mb-2 skill-item';

            const input = document.createElement('input');
            input.type = 'text';
            input.name = 'skills';
            input.className = 'form-control skill-input';
            input.placeholder = 'Ex: Python';
            input.value = value;

            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-outline-danger btn-remove';
            btn.title = 'Supprimer';
            btn.innerHTML = '×';

            wrapper.appendChild(input);
            wrapper.appendChild(btn);
            return wrapper;
        }

        // Pour chaque conteneur skills-list sur la page
        document.querySelectorAll('#skills-list').forEach(function (skillsList) {
            // recherche du bouton "+ Plus" dans le même parent (structure des templates)
            const addBtn = skillsList.parentElement.querySelector('#add-skill') ||
                           skillsList.parentElement.querySelector('.add-skill');

            // Délégation : gestion des clics sur les boutons de suppression
            skillsList.addEventListener('click', function (e) {
                const rem = e.target.closest('.btn-remove');
                if (rem) {
                    e.preventDefault();
                    const item = rem.closest('.skill-item');
                    if (item) item.remove();
                }
            });

            // Si des boutons remove déjà rendus côté serveur, pas besoin d'attacher individuellement (délégation gère)
            // Gestion du bouton "+ Plus"
            if (addBtn) {
                addBtn.addEventListener('click', function (e) {
                    e.preventDefault();
                    const item = createSkillItem('');
                    skillsList.appendChild(item);
                    const input = item.querySelector('.skill-input');
                    if (input) input.focus();
                });
            }

            // Avant l'envoi du formulaire : nettoyer inputs vides et trim les valeurs
            const parentForm = skillsList.closest('form');
            if (parentForm) {
                parentForm.addEventListener('submit', function () {
                    skillsList.querySelectorAll('.skill-input').forEach(input => {
                        if (!input.value || !input.value.trim()) {
                            input.closest('.skill-item')?.remove();
                        } else {
                            input.value = input.value.trim();
                        }
                    });
                });
            }
        });
    }());

    // utilitaire : créer un item skill
    function createSkillItem(value = '') {
        const wrapper = document.createElement('div');
        wrapper.className = 'input-group mb-2 skill-item';

        const input = document.createElement('input');
        input.type = 'text';
        input.name = 'skills';
        input.className = 'form-control skill-input';
        input.placeholder = 'Ex: Python';
        input.value = value;

        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-outline-danger btn-remove';
        btn.title = 'Supprimer';
        btn.innerHTML = '×';

        wrapper.appendChild(input);
        wrapper.appendChild(btn);
        return wrapper;
    }

    // Gérer tous les conteneurs possibles (id ou class)
    document.querySelectorAll('#skills-list, .skills-list').forEach(function (skillsList) {
        // trouver le bouton "add" proche (dans le même parent) - supporte id et class
        let addBtn = null;
        const parent = skillsList.parentElement;
        if (parent) {
            addBtn = parent.querySelector('#add-skill') || parent.querySelector('.add-skill') || parent.querySelector('[data-add-skill]');
        }
        // si pas trouvé dans le parent, chercher globalement (fallback)
        if (!addBtn) {
            addBtn = document.querySelector('#add-skill') || document.querySelector('.add-skill') || document.querySelector('[data-add-skill]');
        }

        // délégation pour suppression (fonctionnera pour boutons existants et ajoutés)
        skillsList.addEventListener('click', function (e) {
            const rem = e.target.closest('.btn-remove');
            if (rem) {
                e.preventDefault();
                const item = rem.closest('.skill-item');
                if (item) item.remove();
            }
        });

        // clic sur "+ Plus"
        if (addBtn) {
            addBtn.addEventListener('click', function (e) {
                e.preventDefault();
                const item = createSkillItem('');
                skillsList.appendChild(item);
                // focus sur le dernier input
                const inputs = skillsList.querySelectorAll('.skill-input');
                const last = inputs[inputs.length - 1];
                if (last) last.focus();
            });
        }

        // nettoyage avant soumission : trim + suppression des vides
        const parentForm = skillsList.closest('form');
        if (parentForm) {
            parentForm.addEventListener('submit', function () {
                skillsList.querySelectorAll('.skill-input').forEach(input => {
                    if (!input.value || !input.value.trim()) {
                        input.closest('.skill-item')?.remove();
                    } else {
                        input.value = input.value.trim();
                    }
                });
            });
        }
    });

    // (Conserver ici d'autres handlers existants — p.ex. animations, search validation, etc.)
});