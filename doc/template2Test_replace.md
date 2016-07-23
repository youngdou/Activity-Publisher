# Some RegExp for test front-end

> we know that when we write the html and link to the css/js file in local file
> we may use some code like "<link src="../static/css/temp.css"/>"
> but when we test the html in server, we have to modify above string to be "<link src="{{ static_url("css/temp.css") }}"/>"
> here is some regexp to use in sublime Text to replace the static-url in a short and stable way

## `../static` to `static_url("")`

1. ctrl+h
2. find: `\{\{ ?static_url\("` and replace with `../static/`
3. find: `"\) ?\}\}` and replace with ``(empty string)

## `static_url("")` to `../static`

1. ctrl+h
2. find: `../static/` and replace with `{{ static_url("`
3. find: `\.png`(`\.css` or `\.js` and so on) and replace with `.png") }}`(`.css") }}` or `.js") }}` and so on)(empty string)

