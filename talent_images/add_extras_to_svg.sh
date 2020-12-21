cp svgs/* ./svgs_with_extras

for elt in ./svgs_with_extras/*.svg; do sed -i -e's/<defs>/<defs><clipPath id="clip"><circle cx="0" cy="0" r="29" \/><\/clipPath>/' -e's_</defs>_</defs><circle cx="0" cy="0" r="32" fill="#331104" /><circle cx="0" cy="0" r="31.4" fill="#73270B" /><circle cx="0" cy="0" r="30.2" fill="#9A340E" /><circle cx="0" cy="0" r="29.6" fill="#4c1804" />_' $elt; done
