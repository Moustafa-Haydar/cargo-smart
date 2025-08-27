<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Role;
class RoleSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        Role::firstOrCreate(['name' => 'admin'], ['description' => 'System administrator']);
        Role::firstOrCreate(['name' => 'ops_manager'], ['description' => 'Operations Manager']);
        Role::firstOrCreate(['name' => 'analyst'], ['description' => 'Data Analyst']);
    }
}
