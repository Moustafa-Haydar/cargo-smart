<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('operations', function (Blueprint $table) {
            $table->id();
            $table->string('name')->unique(); // read, create, update, delete, export...
            $table->timestamps();
        });
    }
    public function down(): void
    {
        Schema::dropIfExists('operations');
    }
};
