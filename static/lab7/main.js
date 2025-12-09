function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i<films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitleRus = document.createElement('td');
            let tdTitle = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitleRus.innerText = films[i].title_ru;
            
            if (films[i].title) {
                tdTitle.innerHTML = '<i style="color: gray;">(' + films[i].title + ')</i>';
            } else {
                tdTitle.innerText = '';
            }
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'Редактировать'
            editButton.onclick = function() {
                editFilm(i);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;

        // Очищаем ошибки
        document.getElementById('title-error').textContent = '';
        document.getElementById('title-ru-error').textContent = '';
        document.getElementById('year-error').textContent = '';
        document.getElementById('description-error').textContent = '';
        showModal();
    });
}

//функция удаления фильма
function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить данный фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList()
        });
}
//функции показа и скрытия блока параметров
function showModal() {
    document.querySelector('div.modal').style.display = 'block';
    document.getElementById('description-error').innerText = '';
}
function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}
function cancel() {
    hideModal();
}
function addFilm() {
    showModal();
}


function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';

    // Очищаем ошибки
    document.getElementById('title-error').textContent = '';
    document.getElementById('title-ru-error').textContent = '';
    document.getElementById('year-error').textContent = '';
    document.getElementById('description-error').textContent = '';
    showModal();
}


function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: parseInt(document.getElementById('year').value) || 0,
        description: document.getElementById('description').value,
    }

    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST': 'PUT';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        //Очищаем поля с ошибками
        document.getElementById('title-error').textContent = '';
        document.getElementById('title-ru-error').textContent = '';
        document.getElementById('year-error').textContent = '';
        document.getElementById('description-error').textContent = '';

        if (errors) {
        // Ошибка для английского названия
        if (errors.title) {
            document.getElementById('title-error').textContent = errors.title;
        }
        
        // Ошибка для русского названия  
        if (errors.title_ru) {
            document.getElementById('title-ru-error').textContent = errors.title_ru;
        }
        
        // Ошибка для года
        if (errors.year) {
            document.getElementById('year-error').textContent = errors.year;
        }
        
        // Ошибка для описания
        if (errors.description) {
            document.getElementById('description-error').textContent = errors.description;
        }
        }    
    })
};