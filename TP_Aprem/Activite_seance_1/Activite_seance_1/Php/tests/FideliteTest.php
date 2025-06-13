<?php

use PHPUnit\Framework\TestCase;

require_once __DIR__ . '/../src/fidelite.php';

class FideliteTest extends TestCase
{
    public function testClientNonVip() {
        $this->assertEquals(4, calculerPointsFidelite(45, false));
        $this->assertEquals(0, calculerPointsFidelite(5, false));
    }

    public function testClientVip() {
        $this->assertEquals(8, calculerPointsFidelite(45, true));
        $this->assertEquals(0, calculerPointsFidelite(9.99, true));
    }
}
