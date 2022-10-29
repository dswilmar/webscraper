create table categorias(
	id serial primary key,
	nome varchar(100),
	url varchar(255),
	processada int default 0
);

create table empresas(
	id serial primary key,
	nome varchar(120),
	telefone varchar(30),
	endereco varchar(255),
	site varchar(255),
	fb varchar(255),
	ig varchar(255),
	url varchar(255)
);