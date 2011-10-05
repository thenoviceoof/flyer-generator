// front

$(document).ready(function(){
    $("li.event").click(function(e){
        var obj = $(e.target);
        while(obj.parent()[0] != $("ul")[0])
            obj = obj.parent();
        var t = obj.find(".data").text()
        t = t.trim();
        console.log(t);

        var form = $("<form>")
            .attr("method","POST")
            .attr("action","/event")
	; 
        var input = $("<input>")
            .attr("type","hidden")
            .attr("name","data")
            .attr("value",t)
        ;
        form.append(input);
	// handle firefox fickleness
	$("body").append(form);
        form.submit();
    });
});