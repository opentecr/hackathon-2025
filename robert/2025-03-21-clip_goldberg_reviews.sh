if true; then
	mkdir part1
cd    part1

pdfseparate ~/opentecr_lit_crawl/the_full_goldberg_reviews/part\ 1.pdf %d.pdf

for i in {9..59..2}; do pdfcrop --margins '-80 -40 -270 -60' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {9..59..2}; do pdfcrop --margins '-340 -40 -20 -60' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {10..60..2}; do pdfcrop --margins '-40 -40 -320 -60' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {10..60..2}; do pdfcrop --margins '-290 -40 -60 -60' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {9..60}; do
pdfunite ${i}_clipped1.pdf ${i}_clipped2.pdf ${i}_merged_clip.pdf
done
pdfunite {9..60}_merged_clip.pdf out.pdf

mv out.pdf ../part1_clipped.pdf
fi;

if false; then
mkdir part2
cd    part2

pdfseparate ~/opentecr_lit_crawl/the_full_goldberg_reviews/part\ 2.pdf %d.pdf

for i in {5..61..2}; do pdfcrop --margins '-20 -20 -300 -0' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {5..61..2}; do pdfcrop --margins '-270 -20 -50 -20' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {4..60..2}; do pdfcrop --margins '-50 -10 -270 -20' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {4..60..2}; do pdfcrop --margins '-300 -10 -20 -20' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {4..61}; do
pdfunite ${i}_clipped1.pdf ${i}_clipped2.pdf ${i}_merged_clip.pdf
done
pdfunite {4..61}_merged_clip.pdf out.pdf

mv out.pdf ../part2_clipped.pdf
fi
