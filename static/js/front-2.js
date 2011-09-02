var fonts = [
    ["Serif",
     ["Droid Serif",
      "Cousine",
      "OFL Sorts Mill Goudy TT",
      "Vollkorn",
      "Crimson Text",
      "Arvo"]],
    ["Sans Serif",
     ["Droid Sans",
      "Nobile",
      "Molengo",
      "PT Sans",
      "Inconsolata",
      "Droid Sans Mono",
      "Josefin Slab"]],
    ["Other",
     ["Tangerine",
      "Philosopher",
      "Lobster",
      "Reenie Beanie"]]];

// loads Fonts dynamically
// http://www.hunlock.com/blogs/Howto_Dynamically_Insert_Javascript_And_CSS
function loadFont(fontName) {
    var head = document.getElementsByTagName("head")[0];
    var style = document.createElement("link");
    style.type="text/css";
    style.rel ="stylesheet";
    style.href="http://fonts.googleapis.com/css?family="+fontName.replace(" ","+");
    head.appendChild(style);
}

// keep everything in the closure
$(function() {
    $("#editor").dialog({
        autoOpen: false,
        width: "auto",
        title: "Flyer Generator r004"
    });
    $("#date").datepicker({ showButtonPanel:true, numberOfMonths: 2 });

    // otherwise, only changes on blur/focus
    $("input, textarea").keyup(function() { 
        $(this).change() 
    });
    $("input, textarea").change(function() {
        var data = $(this).val();
        var d = data.replace(/\n/g,"<br/>");
        $("#"+$(this).attr("id")+"_body").html(d);
    });

    var debug = false;
    $("#debug").click(function(event) {
        if(debug) {
            $("body").css("border","");
            debug = false;
        } else {
            $("body").css("border","1px black solid");
            debug = true;
        }
    });

    // handle some specific changes on changing date formats
    $("#format").change(function() {
        $("#date").datepicker( "option", "dateFormat", $(this).val() );
        $("#date").datepicker("refresh");
        $("#date").change();
    });

    // set up way to reopen dialog in a non-intrusive way
    $("body").dblclick(function() {
        $("#editor").dialog("open");
        return false;
    });

    // load fonts
    for(var fam in fonts) {
        for(var f in fonts[fam][1]) {
            loadFont(fonts[fam][1][f]);
        }
    }
    // add fonts to the font chooser
    for(var fam in fonts) {
        var family = fonts[fam][0];
        for(var f in fonts[fam][1]) {
            var font = fonts[fam][1][f];
            var header = $("<h3></h3>").html(family+" - "+font);
            header.css("font-family",font);
            $("#fontChooser").append(header);
            var example = $("<div></div>").html("abcdefghijklmnopqrstuvwxyz0123456789");
            example.css("font-family",font);
            $("#fontChooser").append(example);
            header.data('font',font);
            example.data('font',font);
        }
    }

    // and some jq styling
    $("#styleEditor").dialog({title:"Style Editor",autoOpen:false,model:true,width:'auto'});
    $("#styler").click(function(){
        $("#styleEditor").dialog("open");
    });
    $("#fontChooser").accordion({autoHeight:false});
    $("#fontFamily").click(function(){
        $("#fontChooserContainer").toggle();
    });
    $("#fontChooser > h3, #fontChooser > div").dblclick(function(){
        $("#page").css("font-family",$(this).data('font'));
        $("#fontChooserContainer").hide();
        return false;
    });
});