import approvals = require('approvals');
(approvals as any).configure({ reporters: ['nodediff'] });

(approvals as any).configure({
    reporters: ['nodediff'],
    failOnLineEndingDifferences: false   
  });
  