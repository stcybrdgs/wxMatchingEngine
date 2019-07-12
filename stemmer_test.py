import jellyfish

s = 'My doctors are both single students who like sandwiches.'

print('Before: ', s)

start = 0
end = 0
nu_s = ''
for char in s:
    if char = ' ':
        print('Stemming ', s[start:end])
        nu_s = nu_s + jellyfish.porter_stem(s[start:end]) + ' '
        start = end
    end += 1

print('After: ', nu_s)

print('Done.')
