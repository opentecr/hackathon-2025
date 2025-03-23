if false; then
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



if false; then
mkdir part3
cd    part3

pdfseparate ~/opentecr_lit_crawl/the_full_goldberg_reviews/part\ 3.pdf %d.pdf

for i in {5..61..2}; do pdfcrop --margins '-60 -40 -290 -30' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {5..61..2}; do pdfcrop --margins '-320 -60 -40 -30' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {6..62..2}; do pdfcrop --margins '-70 -60 -290 -30' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {6..62..2}; do pdfcrop --margins '-320 -40 -40 -30' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {5..62}; do
pdfunite ${i}_clipped1.pdf ${i}_clipped2.pdf ${i}_merged_clip.pdf
done
pdfunite {5..62}_merged_clip.pdf out.pdf

mv out.pdf ../part3_clipped.pdf
fi


if false; then
mkdir part4
cd    part4

pdfseparate ~/opentecr_lit_crawl/the_full_goldberg_reviews/part\ 4.pdf %d.pdf

for i in {5..25..2}; do pdfcrop --margins '-80 -40 -280 -30' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {5..25..2}; do pdfcrop --margins '-330 -60 -20 -30' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {6..26..2}; do pdfcrop --margins '-40 -60 -320 -30' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {6..26..2}; do pdfcrop --margins '-290 -40 -70 -30' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {5..26}; do
pdfunite ${i}_clipped1.pdf ${i}_clipped2.pdf ${i}_merged_clip.pdf
done
pdfunite {5..26}_merged_clip.pdf out.pdf

mv out.pdf ../part4_clipped.pdf
fi

if false; then
mkdir part5
cd    part5

pdfseparate ~/opentecr_lit_crawl/the_full_goldberg_reviews/part\ 5.pdf %d.pdf

for i in {5..31..2}; do pdfcrop --margins '-100 -50 -260 -50' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {5..31..2}; do pdfcrop --margins '-360 -60 -20 -50' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {6..30..2}; do pdfcrop --margins '-80 -60 -290 -50' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {6..30..2}; do pdfcrop --margins '-320 -70 -50 -50' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {5..31}; do
pdfunite ${i}_clipped1.pdf ${i}_clipped2.pdf ${i}_merged_clip.pdf
done
pdfunite {5..31}_merged_clip.pdf out.pdf

mv out.pdf ../part5_clipped.pdf
fi


if false; then
mkdir part6
cd    part6

pdfseparate ~/opentecr_lit_crawl/the_full_goldberg_reviews/part\ 6.pdf %d.pdf

for i in {5..27..2}; do pdfcrop --margins '-30 -0 -260 -30' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {5..27..2}; do pdfcrop --margins '-300 -0 10 -30' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {6..28..2}; do pdfcrop --margins '-30 -0 -260 -30' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {6..28..2}; do pdfcrop --margins '-300 -0 10 -30' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {5..28}; do
pdfunite ${i}_clipped1.pdf ${i}_clipped2.pdf ${i}_merged_clip.pdf
done
pdfunite {5..28}_merged_clip.pdf out.pdf

mv out.pdf ../part6_clipped.pdf
fi


if true; then
mkdir part7
cd    part7

pdfseparate ~/opentecr_lit_crawl/the_full_goldberg_reviews/part\ 7.pdf %d.pdf

for i in {5..41..2}; do pdfcrop --margins '10 -30 -260 -40' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {5..41..2}; do pdfcrop --margins '-260 -0 10 -40' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {6..40..2}; do pdfcrop --margins '10 -0 -260 -40' --clip ${i}.pdf ${i}_clipped1.pdf; done
for i in {6..40..2}; do pdfcrop --margins '-260 -30 10 -40' --clip ${i}.pdf ${i}_clipped2.pdf; done

for i in {5..41}; do
pdfunite ${i}_clipped1.pdf ${i}_clipped2.pdf ${i}_merged_clip.pdf
done
pdfunite {5..41}_merged_clip.pdf out.pdf

mv out.pdf ../part7_clipped.pdf
fi
