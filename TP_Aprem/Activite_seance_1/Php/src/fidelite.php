<?php

function calculerPointsFidelite(float $montant, bool $isVip): int {
    $points = floor($montant / 10);
    if ($isVip) {
        $points *= 2;
    }
    return $points;
}
