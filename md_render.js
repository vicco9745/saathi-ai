function mdInline(s){
var c=(s.match(/\*\*/g)||[]).length;if(c%2)s+='**';
var b=(s.match(/`/g)||[]).length;if(b%2)s+='`';
var codes=[];
s=s.replace(/`([^`]+)`/g,function(_,x){codes.push(x);return '\u0001'+(codes.length-1)+'\u0002';});
s=s.replace(/\*\*([^*]+?)\*\*/g,'<strong>$1</strong>');
s=s.replace(/(^|[^*\w])\*([^*\s](?:[^*\n]*[^*\s])?)\*(?![*\w])/g,'$1<em>$2</em>');
s=s.replace(/(https?:\/\/[^\s<]+)/g,function(u){return '<a href="'+u+'" target="_blank" rel="noopener noreferrer" class="msg-link">'+u+'</a>';});
s=s.replace(/\u0001(\d+)\u0002/g,function(_,i){return '<code class="md-ic">'+codes[+i]+'</code>';});
return s;}
function mdRender(text){
var lines=escapeHtml(String(text==null?'':text)).split('\n'),out=[],i=0,list=null,SP='<div class="md-sp"></div>';
function close(){if(list){out.push('</'+list+'>');list=null;}}
function cells(r){r=r.trim();if(r.charAt(0)==='|')r=r.slice(1);if(r.charAt(r.length-1)==='|')r=r.slice(0,-1);return r.split('|').map(function(x){return x.trim();});}
var sepRe=/^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/;
while(i<lines.length){
var l=lines[i],m;
if(/^\s*\|/.test(l)&&i+1<lines.length&&sepRe.test(lines[i+1])){
close();var head=cells(l);i+=2;var rows=[];
while(i<lines.length&&/^\s*\|/.test(lines[i])){rows.push(cells(lines[i]));i++;}
out.push('<div class="md-tw"><table class="md-t"><thead><tr>'+head.map(function(x){return '<th>'+mdInline(x)+'</th>';}).join('')+'</tr></thead><tbody>'+rows.map(function(r){return '<tr>'+r.map(function(x){return '<td>'+mdInline(x)+'</td>';}).join('')+'</tr>';}).join('')+'</tbody></table></div>');
continue;}
if(/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(l)){close();out.push('<hr class="md-hr">');}
else if((m=/^\s*(#{1,6})\s+(.*)$/.exec(l))){close();out.push('<div class="md-h md-h'+m[1].length+'">'+mdInline(m[2].replace(/\s+#+\s*$/,''))+'</div>');}
else if((m=/^\s*&gt;\s?(.*)$/.exec(l))){close();out.push('<div class="md-q">'+mdInline(m[1])+'</div>');}
else if((m=/^\s*[-*\u2022]\s+(.*)$/.exec(l))){if(list!=='ul'){close();out.push('<ul class="md-l">');list='ul';}out.push('<li>'+mdInline(m[1])+'</li>');}
else if((m=/^\s*(\d+)[.)]\s+(.*)$/.exec(l))){if(list!=='ol'){close();out.push('<ol class="md-l" start="'+m[1]+'">');list='ol';}out.push('<li>'+mdInline(m[2])+'</li>');}
else if(l.trim()===''){close();if(out.length&&out[out.length-1]!==SP)out.push(SP);}
else{close();out.push('<div class="md-p">'+mdInline(l)+'</div>');}
i++;}
close();return out.join('');}
if(typeof module!=='undefined'){module.exports={mdRender:mdRender};}
