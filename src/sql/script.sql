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

--remover registros duplicados na tabela de empresas
select * from empresas a
where exists (select 1 from empresas b where a.nome = b.nome and a.id < b.id)