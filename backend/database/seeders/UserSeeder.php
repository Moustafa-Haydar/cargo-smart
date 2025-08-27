<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\User;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        User::firstOrCreate([
            'first_name' => 'Moustafa',
            'last_name' => 'Haydar',
            'email' => 'moustafahaydar.eng@gmail.com',
            'username' => 'admin',
            'password' => bcrypt('ssssssss'),
            'role_id' => '1',
        ]);
    }
}
