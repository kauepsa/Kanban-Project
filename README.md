# Projeto Kanban
Este é um projeto que simula um quadro Kanban , onde o usuário pode criar grupos (projetos) e junto com outros usuários , criar colunas e tarefas para gerenciar seus projetos . 

# Tecnologias Utilizadas
* Python 
* Django
* HTML+CSS
* JavaScript + jQuery
* Bootstrap 5

# Funcionalidades
* Perfil de usuário;
* Verificação de email no cadastro;
* Email de recuperação de senha;
* Permite criar grupos , colunas , tarefas;
* Design responsivo

![image](https://github.com/kauepsa/Kanban-Project/assets/93888091/5e4f07cb-523c-4562-bfb8-b1b85b1a6618)
![image](https://github.com/kauepsa/Kanban-Project/assets/93888091/fd6141ce-cc13-4a1a-9f1c-714e93c15402)
![image](https://github.com/kauepsa/Kanban-Project/assets/93888091/df4207e4-5a36-42ec-a48a-9b8308742b59)
![image](https://github.com/kauepsa/Kanban-Project/assets/93888091/ce8a912f-11a3-4a7b-8ef5-181ab8e2d008)
![image](https://github.com/kauepsa/Kanban-Project/assets/93888091/6e901620-50d6-4a4e-a778-8fcbfa9a3f3a)
![image](https://github.com/kauepsa/Kanban-Project/assets/93888091/afb197fd-24af-42a4-96d0-3bfe7c1d1d12)
![image](https://github.com/kauepsa/Kanban-Project/assets/93888091/8ba1f164-b1e7-418e-8972-d04b6d43c3ff)
![image](https://github.com/kauepsa/Kanban-Project/assets/93888091/b4a8e375-f54b-4d49-b85f-48d29560c19b)
![image](https://github.com/kauepsa/Kanban-Project/assets/93888091/c6932322-04b7-44e7-b9d1-d8699e6980f4)
![mobile version](https://github.com/kauepsa/Kanban-Project/assets/93888091/98e9789f-ff77-4433-a61c-bc317db54e46)



# Instalação
* Clone o repositório do GitHub para sua máquina local. Você pode fazer isso usando o comando git clone e o URL do repositório: <br>
```git clone https://github.com/kauepsa/Kanban-Project```

* Certifique-se de que o Python e pip estão instalados em sua máquina. Você pode verificar isso executando o seguinte comando: <br>
```python --version``` <br>
```pip --version``` <br>

* Crie um ambiente virtual para isolar as dependências do projeto. Você pode fazer isso executando o comando a seguir: <br>
```python -m venv myvenv``` 

* Ative o ambiente virtual executando o comando abaixo (para Windows): <br>
```seu-caminho-de-diretorio/Kanban-Project/venv/Scripts/Activate.ps1```

* (para MacOS e Linux): <br>
```source myvenv/bin/activate```

* Instale as dependências do projeto usando o arquivo requirements.txt que está no repositório. Você pode fazer isso executando o comando: <br>
```pip install -r requirements.txt```

* Configure o banco de dados caso deseje utilizar algum outro além do Sqlite3 (Banco de dados padrão do Django).

* Execute as migrações do banco de dados. Você pode fazer isso executando o comando abaixo: <br>
```python manage.py makemigrations``` <br>
```python manage.py migrate```

* Crie um superusuário para acessar o painel de administração do Django. Você pode fazer isso executando o comando: <br>
```python manage.py createsuperuser```

* Inicie o servidor local executando o comando 'runserver': <br>
```python manage.py runserver```

* Abra o navegador e navegue até http://localhost:8000 para visualizar o projeto. Se desejar acessar o painel de administração , você pode acessá-lo em http://localhost:8000/admin usando as credenciais do superusuário que você criou anteriormente.
