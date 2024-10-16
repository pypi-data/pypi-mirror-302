kthutils config forms.rewriter.restlabb -s ""
kthutils config forms.rewriter.restlabb.format_string -s "
echo 'Course:       {course}'
echo 'Module:       {module}'
echo 'Student:      {student}'
echo 'Comments:     {comments}'
echo 'Grader:       {grader}'
canvaslms grade \
  -c '{course_code} {semester}' \
  -a '{assignment}' \
  -u '{student}' \
  -g '{grade}' \
  -m 'OK {grader}'
echo 'Canvas:'
canvaslms submissions \
  -c '{course_code} {semester}' \
  -a '{assignment}' \
  -u '{student}'
echo
"
kthutils config forms.rewriter.restlabb.substitutions.module.column -s 5
kthutils config forms.rewriter.restlabb.substitutions.comments.column -s 6
kthutils config forms.rewriter.restlabb.substitutions.course.column -s 3
kthutils config forms.rewriter.restlabb.substitutions.course_code.column -s 3
kthutils config forms.rewriter.restlabb.substitutions.course_code.regex \
  -s "s/^.*([A-Z]{2}\d{3,4}[A-Z]?).*$/\1/"
kthutils config forms.rewriter.restlabb.substitutions.semester.column -s 3
kthutils config forms.rewriter.restlabb.substitutions.semester.regex \
  -s "s/^.*[Hh][Tt](\d{2}).*$/HT\1/" \
  -s "s/^.*[Vv][Tt](\d{2}).*$/VT\1/"
kthutils config forms.rewriter.restlabb.substitutions.grader.column -s 11
kthutils config forms.rewriter.restlabb.substitutions.grader.regex \
  -s "s/^.*?([A-Za-z0-9]+@kth.se).* $/\1/"
kthutils config forms.rewriter.restlabb.substitutions.student.column -s 2
kthutils config forms.rewriter.restlabb.substitutions.student.regex \
  -s "s/^.*?([A-Za-z0-9]+@kth.se).*$/\1/"
kthutils config forms.rewriter.restlabb.substitutions.grade.column -s 5
kthutils config forms.rewriter.restlabb.substitutions.grade.regex \
  -s "s/.*([Bb]etyg|,)?\b([A-F])(\b.*)?$/\2/" \
  -s "s/.*EJ GODKÄN[TD].*$/F/"
kthutils config forms.rewriter.restlabb.substitutions.grade.no_match_default \
  -s P
kthutils config forms.rewriter.restlabb.substitutions.assignment.column -s 5
kthutils config forms.rewriter.restlabb.substitutions.assignment.regex \
  -s 's/.*[Ss][Pp][Ee][Cc].*/spec/' \
  -s 's/.*[Gg](ransk|RANSK).*/granskning/' \
  -s 's/.*[Pp](-?upp(gift)?|rojekt(?!spec|gransk)).*/redovisning/' \
  -s 's/.*[Ll]ab(?:b|oration)? *(\d-\d)\D*.*/Laboration..[\1]./' \
  -s 's/.*[Ll]ab(?:b|oration)? *(\d+(?:\s*(?:[,&+]| och | å )\s*\d+)*)\D*.*/Laboration .(\1)./; s/\s*(?:[,&+]| och | å )\s*/|/'
