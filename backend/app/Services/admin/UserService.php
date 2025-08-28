<?php
namespace App\Services\Admin;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use App\Http\Requests\StoreUserRequest;

class UserService
{

    public static function getAllUsers($id = null)
    {
        if ($id == null) {
            return User::all();
        }
        return User::find($id);
    }
    public static function addUser(Request $request)
    {
        $data = $request->validated();
        $data['password'] = Hash::make($data['password']);
        $user = User::create($data);
        return ($user);
    }

    public static function deleteAllUsers($id = null)
    {
        if ($id == null) {
            // delete all users
            return User::truncate();
        }

        $user = User::find($id);
        if (!$user) {
            // User not found
            return false;
        }

        // Delete the user with the given ID
        return $user->delete();
    }

}