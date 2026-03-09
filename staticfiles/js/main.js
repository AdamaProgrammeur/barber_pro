// Exemple CRUD Clients
const API_URL_CLIENTS = '/api/clients/';

async function loadClients(){
    const res = await fetch(API_URL_CLIENTS);
    const data = await res.json();
    const tbody = document.querySelector('#clientsTable tbody');
    tbody.innerHTML = '';
    data.forEach(c=>{
        tbody.innerHTML += `<tr>
            <td>${c.nom}</td>
            <td>${c.telephone}</td>
            <td>
                <button class="btn btn-warning btn-sm" onclick="editClient(${c.id})">Modifier</button>
                <button class="btn btn-danger btn-sm" onclick="deleteClient(${c.id})">Supprimer</button>
            </td>
        </tr>`;
    });
}

document.getElementById('addClientForm')?.addEventListener('submit', async e=>{
    e.preventDefault();
    const nom = document.getElementById('nom').value;
    const telephone = document.getElementById('telephone').value;

    await fetch(API_URL_CLIENTS, {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({nom,telephone})
    });
    loadClients();
    new bootstrap.Modal(document.getElementById('addClientModal')).hide();
});

async function editClient(id){
    const nom = prompt("Nouveau nom:");
    const telephone = prompt("Nouveau téléphone:");
    await fetch(`${API_URL_CLIENTS}${id}/`, {
        method:'PUT',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({nom,telephone})
    });
    loadClients();
}

async function deleteClient(id){
    if(confirm("Supprimer ce client ?")){
        await fetch(`${API_URL_CLIENTS}${id}/`, {method:'DELETE'});
        loadClients();
    }
}

document.addEventListener('DOMContentLoaded', loadClients);
