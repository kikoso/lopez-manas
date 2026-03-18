---
date: '2008-02-19T11:46:21+00:00'
draft: false
slug: crear-imagenes-de-windows-xp-con-ghost-y-sysprep
title: Crear imágenes de Windows XP con Ghost y Sysprep
---

Generalmente, tiendo a instalar y reinstalar sistemas operativos con bastante frecuencia. Con mi horario tan infernal, no dispongo del tiempo suficiente para sentarme y reinstalar y configurar hasta el último programa. Aunque es relativamente fácil usar un backup de mi sistema para el trabajo diario, tiendo a cambiar periféricos con bastante frecuencia, y restaurar un sistema del que no se han eliminado ciertos drivers tiende a causar estragos en una nueva configuración. Para hacer este proceso más rápido, he creado una imagen fantasma de mi disco duro después de realizar una instalación básica. Ahora, en lugar de tener que invertir unas cuantas horas para dejar un sistema a punto, puedo hacer eso en 15 minutos con solo 6 clicks de ratón. El truco para esto es utilizar Norton Ghost o cualquier otro software de imagen y Microsoft Sysprep.

<!--more-->

Paso 1: Instalación de XP y Sysprep
<ol>
	<li>Instala Windows XP en un disco duro formateado (nada de sobreinstalaciones)</li>
	<li>No instales ningún driver o aplicaciones dependientes del hardware más allá de las que el propio Windows tenga que instalar.
<ul>
	<li>Esto es necesario para asegurarse de que la imagen es exportable a diferentes tipos de sistemas. A pesar de ello, diferentes controladores de almacenamiento hacen esto difícil de predecir.</li>
	<li>La mayoría de los ordenadores más modernos trabajan bien con una ACPI HAL estándar, pero si esta imagen es para ser verdaderamente portable a varias máquinas, entonces debe determinarse qué HAL específica se necesita. Si estás completamente perdido, puedes echar un ojo a <a href="http://support.microsoft.com/kb/309283/" title="Microsoft Knowledge Base: Article #309283">Microsoft KB309283</a>.
<ul>
	<li>También es importante determinar si el sistema objetivo usa un controlador de almacenamiento que normalmente requiera un disco de drivers durante una instalación regular de XP. Si este es el caso, entonces los paths necesarios a los drivers deberán ser incluidos en el fichero Sysprep.inf. Esto debe ser añadido a <code>[SysprepMassStorage]</code> dentro de <code>PCI\\VEN_###&amp;DEV_#### = PATH_TO_DRIVER_ON_IMAGED_DRIVE</code>, donde VEN_#### deberá ser sustituido por el ID del fabricante (i.e. VEN_1234) , y DEV_#### deberá ser sustituido por el ID del dispositivo (DEV_1234). Esta información se puede encontrar en los archivos de driver INF. Este es un ejemplo de cómo añadir el controlador SCSI de VMWARE a sysprep.inf<code>:</code>
<blockquote> [SysprepMassStorage]

PCI\\VEN_104B&amp;DEV_1040=C:\\Drivers\\Mass\\VMWare\\vmscsi.inf</blockquote>
</li>
</ul>
</li>
</ul>
</li>
	<li>Crear una cuenta <code>test</code> con privilegios administrativos. Usar esta cuenta para instalar y configurar todo el software y todas las políticas de tu sistema</li>
	<li>Recuerda actualizar Windows, Office y el resto del software. Probablemente tendrás que reiniciar unas cuantas veces entre medias, pero asegúrate de que todo el sistema se ha actualizado.</li>
	<li>Copia todo el menú de inicio de la cuenta <code>test</code> al menú de inicio de <code>Administrador</code>. (<strong>Nota:</strong> Esto es necesario porque algunos instaladores no crean accesos directos en el menú inicio para todos los usuarios, sino tan sólo para aquel donde se ha instalado.)</li>
	<li>Desloguéate y vuélvete a loguear como administrador, y copia todo el directorio de perfil del usuario test al directorio de perfil del usuario por defecto. Esto se puede hacer mediante Panel de Control -&gt; Sistema -&gt; Avanzado -&gt; Configuración del perfil de usuario, selecciona al usuario test, y copia. Copia todo esto a  <code>c:\\Documents and Settings\\Default User</code>. Si te has perdido puedes echar un ojo a <a href="http://support.microsoft.com/kb/291586/" title="Microsoft Knowledge Base: Article #291586">Microsoft KB291586</a>.</li>
	<li>Borra la cuenta <code>test. </code>Asegúrate de que <code>c:\\Documents and Settings\\testuser</code> está también borrado.</li>
	<li>Descárgate <a href="http://support.microsoft.com/?kbid=838080" title="Microsoft Knowledge Base: SysPrep">Sysprep para XP SP2</a>.</li>
	<li>Extrae el contenido del archivo a <code>c:\\sysprep</code>.</li>
	<li>Crea el fichero básico <code>sysprep.inf</code> ejecutando <code>setupmgr.exe</code>. Los pasos son los siguientes:
<ul>
	<li>Ejecuta setupmgr.exe</li>
	<li>Clic en <em>Create New</em></li>
	<li>Clic en <em>Sysprep Setup</em></li>
	<li>Ahora elige el producto que estés utilizando. En nuestro caso, sería Windows XP Profesional.</li>
	<li>La siguiente pregunta será: <em>¿Quieres automatizar el proceso de instalación?</em> Esta pregunta determina quién va a aceptar el  EULA, tú o la persona que restaure la imagen. Además, escoger sí significa que tienes que introducir también tu número de serie. Escogí no porque esto va a ser para mi propio uso.</li>
	<li>El próximo conjunto de opciones es para que insertes opciones tales como nombre, organización...</li>
	<li>Dejé la opción de Nombre de Equipo establecida a <em>Generar nombre de equipo automáticamente</em>.</li>
	<li>Una vez completado, un cuadro de diálogo te preguntará donde quieres guardar el archivo. La ruta de este ejemplo es c:\\sysprep\\sysprep.inf</li>
	<li>Finalmente, presiona <em>Cancelar</em> para cerrar<code>setupmgr.exe</code>.</li>
</ul>
El proceso de crear un fichero básico <code>sysprep.inf</code> ha terminado</li>
	<li>Antes de continuar con el siguiente paso, crea un directorio de drivers personalizado para cualquier driver que puedas necesitar en el futuro. Generalmente, uso <code>c:\\drivers</code>.</li>
	<li>Abre <code>c:\\sysprep\\sysprep.inf</code> en el blog de notas y añade las siguientes lineas a las secciones más relevantes (si la cabecera no existe, añádela):
<blockquote>[Unattended]
DriverSigningPolicy=Ignore
UpdateInstalledDrivers=Yes
OemPNPDriversPath=drivers\\hardware_cat\\driver_dir\\driver_inf;(repeat);

[SysPrep]
BuildMassStorageSection=Yes

[SysprepMassStorage]</blockquote>
</li>
	<li><strong>¡No cierres <code>sysprep.inf</code> todavía!</strong> OemPNPDriversPath apunta al directorio <code>c:\\drivers</code> creado anteriormente. Con el único objetivo de conseguir una correcta organización, separé mis drivers en función de la categoría (es decir, hardware_cat en el ejemplo superior). Por ejemplo, todos los drivers de video pueden ir bajo <code>c:\\drivers\\video</code> y los drivers de red bajo <code>c:\\drivers\\network</code>. En cada uno de esos directorios, el driver específico será situado con sus ficheros .inf (i.e. driver_dir). Por ejemplo, los últimos nVidia irían dentro de  <code>c:\\drivers\\video\\nVidia\\</code>. La última parte,  <code>driver_inf</code>, es justamente eso, el nombre del fichero .inf. Por ejemplo, para los últimos drivers nVidia, la ruta podría ser <code>c:\\drivers\\video\\nVidia\\nv4_disp.inf</code>. En <code>sysprep.inf</code>, la ruta podría ser escrita como <code>OemPNPDriversPath=drivers\\video\\nVidia\\nv4_disp.inf</code>. Para el siguiente driver, repite el procedimiento colocando la ruta después del igual sin dejar ningún espacio. Una vez que todos los drivers han sido añadidos, salva el fichero.</li>
	<li>Ejecuta <code>c:\\sysprep\\sysprep -bmsd</code>. Esto construirá los drivers de almacenamiento masivo de  Windows XP.</li>
	<li>Mientras editas sysprep.inf verás una opción marcada <code>InstallFilesPath</code>, que usualmente apunta a <code>c:\\sysprep\\i386</code>. Normalmente copio el contenido de mi CD de XP, el directorio i386, dentro de <code>c:\\sysprep\\i386</code>. No obstante, no es necesario.</li>
	<li>Añade cualquier driver de almacenamiento a <code>[SysprepMassStorage]</code> , tal y como se describe más arriba</li>
	<li>Ahora ejecuta <code>C:\\sysprep\\sysprep.exe</code>.</li>
	<li>Elige las opciones <em>Mini Setup</em> y <em>Detect non-plug and play hardware</em>. Si no tienes una licencia de volumen, y sólo planeas usar esta imagen para restablecer el ordenador desde donde has hecho la imagen, entonces selecciona <em>Don’t regenerate security identifiers</em>.</li>
	<li>Asegúrate de que el apagado está seleccionado en el menú <em>Modo de Apagado</em></li>
	<li>Ahora tardará un tiempo, y cuando todo esté listo tu ordenador se reiniciará</li>
</ol>
Sysprep ya está completo. En los próximos días, intentaré escribir instrucciones sobre cómo hacer imágenes de la partición.