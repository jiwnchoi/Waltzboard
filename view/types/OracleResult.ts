export interface OracleResult {
  score: number;
  coverage: number;
  diversity: number;
  specificity: number;
  interestingness: number;
  parsimony: number;
}

export interface OracleSingleResult {
  score: number;
  coverage: number;
  diversity: number;
  specificity: number;
  interestingness: number;
}
