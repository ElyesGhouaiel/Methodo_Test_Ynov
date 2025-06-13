function calculerPointsFidelite(montant, isVip) {
    let points = Math.floor(montant / 10);
    if (isVip) {
      points *= 2;
    }
    return points;
  }
  
  module.exports = calculerPointsFidelite;
  