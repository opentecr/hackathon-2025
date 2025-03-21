pdfseparate ../opentecr_lit_crawl/the_full_goldberg_reviews/part\ 1.pdf %d.pdf

for i in {9..59..2}; do pdfcrop --margins '-80 -40 -270 -60' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {9..59..2}; do pdfcrop --margins '-340 -40 -20 -60' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {10..60..2}; do pdfcrop --margins '-40 -40 -320 -60' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {10..60..2}; do pdfcrop --margins '-290 -40 -60 -60' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {9..60}; do
pdfunite ${i}_clipped1.pdf ${i}_clipped2.pdf ${i}_merged_clip.pdf
done
pdfunite {9..60}_merged_clip.pdf out.pdf
