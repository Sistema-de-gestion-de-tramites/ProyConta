var idList = ["id","nombre","ap_paterno","ap_materno","telefono","dir_num","calle","colonia","delegacion","cod_postal","municipio","estado","pais","correo","estado_civil","fecha_nac","rfc","curp","fecha_reg"];
var outputList = ["# empleado","nombre","apellido paterno","apellido materno","telefono","numero int.","calle","colonia","delegacion","codigo postal","municipio","estado","pais","correo","estado civil","fecha de nacimiento","RFC","curp","fecha registro"];

function map (id,value){
    var div = document.getElementById(id);
    var output_id = document.createElement("output");
    output_id.value=value;
    div.appendChild(output_id);
}

for (var i=0;i<idList.length;i++){
    map(idList[i],outputList[i]);
    map("f_"+idList[i],outputList[i]);
}

