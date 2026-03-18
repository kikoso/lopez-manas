---
date: '2008-03-18T18:44:43+00:00'
draft: false
slug: php-sencillo-sistema-de-login-y-control-de-sesiones
title: PHP- Sencillo sistema de login y control de sesiones
---

He creado un pequeño sistema de login, con control de sesiones, para poder insertar citas mediante una interfaz web en mi base de datos. El sistema es muy básico, pero quizás alguno quiera tener una pequeña referencia al respecto de cómo empezar. Como de costumbre en este mundo de la programación, el único límite es nuestra imaginación, así que el campo de las posibles mejoras aplicables es muy extenso: control del tiempo de login, modelo de factoría para evitar (o permitir) accesos desde múltiples localizaciones, etc.
<!--more-->
En primer lugar, la función para conectar a la base de datos. Ya que será una función que utilizaremos con frecuencia, es una buena elección declararla en un fichero aparte:
<pre lang="php">
function conectar() {
   // Configura los datos de tu cuenta
   $dbhost=''nombre.de.host'';
   $dbusername=''usuario'';
   $dbuserpass=''contraseña'';
   $dbname=''nombreDeBD'';

   // Conectar a la base de datos
   mysql_connect ($dbhost, $dbusername, $dbuserpass);
   mysql_select_db($dbname) or die(''Cannot select database'');
   }</pre>
Típicamente, tendremos un punto de entrada a la aplicación, index.php, en el que colocaremos un formulario con los campos de usuario y contraseña. En el campo action de este formulario, introduciremos la dirección del archivo donde validaremos el login (login.php)
<pre lang="php">
<?php
   conectar();

   // Primero, transformamos los datos recibidos en entidades html para evitar inyecciones sql
    $a_user = htmlentities($_POST[''username''], ENT_QUOTES);
    $a_pass = htmlentities($_POST[''password''], ENT_QUOTES);

    // Ahora creamos una sentencia sql en busca del usuario ingresado:
    $select = mysql_query("SELECT * FROM nt_users WHERE username=''{$a_user}''");
    // Ahora comprobamos que el usuario exista.
    if(mysql_num_rows($select) != 0) {

		// Bien, ahora que sabemos que existe, creamos un bucle para obtener los datos...
    	while($row = mysql_fetch_array($select)) {

    		/* Ahora con los datos obtenidos, comprobamos que la contraseña sea correcta.
    	   	   Hay que recordar que la contraseña guardada está encriptada y no se puede desencriptar.
        	   Para hacer la comprobación, encriptamos la nueva contraseña y la comparamos con la guardada */
    		if(md5($a_pass) == $row[''password'']) {
    			//Variable de sesión de usuario válido
				$validUser= true;
				$_SESSION[''validUser''] = false;
        		$_SESSION[''s_username''] = $a_user;
				echo "Has sido logueado correctamente ".$_SESSION[''s_username'']." y puedes acceder al <a href="/wp-admin/%5C%22formulario.php%5C%22">formulario.php</a>";
		    } else {
				echo ''Nombre de usuario o contraseña inválidos.<a href="javascript:back();"&lt;&lt;"></a>'';
    		}
    		// La siguiente llave cierra el bucle while, no necesita else.
		}
   	} else {
		if ($validUser == true) $_SESSION[''validUser''] = true;
    	else $_SESSION[''validUser''] = false;
  	echo ''Nombre de usuario o contraseña inválidos.<a href="javascript:back();"&lt;&lt;"></a>'';
	}
?&gt;</pre>
 
Finalmente, en formulario.php controlaremos la validez de la sesión abierta, y tomaremos una decisión sobre la validez del usuario que realiza la petición:
<pre lang="php">
<?php
	conectar();
	if (isset($_SESSION[''validUser''])){
    	include("menu.php");

} else{
   		echo "Tu no estas autentificado dirígete a login.php o registrate en register.php";
    }
?> 
</pre>

Siempre tendremos que usar este verificación con isset en las páginas que queremos que estén protegidas por una sesión.